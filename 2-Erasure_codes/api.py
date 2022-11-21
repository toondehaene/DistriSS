from flask import Flask, make_response, g, request, send_file
import sqlite3
import logging

import zmq # For ZMQ
import time # For waiting a second for ZMQ connections
import io # For sending binary data in a HTTP response
import logging
import rs
import threading

from utils import is_raspberry_pi

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'files.db',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Initiate ZMQ sockets
context = zmq.Context()

# Socket to send tasks to Storage Nodes
send_task_socket = context.socket(zmq.PUSH)
send_task_socket.bind("tcp://*:5557")

# Socket to receive messages from Storage Nodes
response_socket = context.socket(zmq.PULL)
response_socket.bind("tcp://*:5558")

# Publisher socket for data request broadcasts
data_req_socket = context.socket(zmq.PUB)
data_req_socket.bind("tcp://*:5559")

# Wait for all workers to start and connect. 
time.sleep(1)
print("Listening to ZMQ messages on tcp://*:5558 and tcp://*:5561")


# Instantiate the Flask app (must be before the endpoint functions)
app = Flask(__name__)
# Close the DB connection after serving the request
app.teardown_appcontext(close_db)

@app.route('/files/<int:file_id>',  methods=['GET'])
def get_file(file_id):

    db = get_db()
    cursor = db.execute("SELECT * FROM `file` WHERE `id`=?", [file_id])
    if not cursor: 
        return make_response({"message": "Error connecting to the database"}, 500)
    
    f = cursor.fetchone()
    if not f:
        return make_response({"message": "File {} not found".format(file_id)}, 404)

    # Convert to a Python dictionary
    f = dict(f)
    print("File requested: {}".format(f['filename']))
    
    # Parse the storage details JSON string
    import json
    storage_details = json.loads(f['storage_details'])

    coded_fragments = storage_details['coded_fragments']
    max_erasures = storage_details['max_erasures']

    file_data, time_to_decode = rs.get_file(
        coded_fragments,
        max_erasures,
        f['size'],
        data_req_socket, 
        response_socket
    )

    # Save measurement on thread
    thread = threading.Thread(target=writeMeasurement("DecodingMeasurements.txt", f['size'], time_to_decode))
    thread.start()

    return send_file(io.BytesIO(file_data), mimetype=f['content_type'])
#

def writeMeasurement(measurementFile, filesize, time):
    file = open(measurementFile, 'a')
    file.write(str(filesize) + " " + str(time)+"\n")
    file.close()


@app.route('/files_mp', methods=['POST'])
def add_files_multipart():
    # Flask separates files from the other form fields
    payload = request.form
    files = request.files
    
    # Make sure there is a file in the request
    if not files or not files.get('file'):
        logging.error("No file was uploaded in the request!")
        return make_response("File missing!", 400)
    
    # Reference to the file under 'file' key
    file = files.get('file')
    # The sender encodes a the file name and type together with the file contents
    filename = file.filename
    content_type = file.mimetype
    # Load the file contents into a bytearray and measure its size
    data = bytearray(file.read())
    size = len(data)
    print("File received: %s, size: %d bytes, type: %s" % (filename, size, content_type))
    
    # Read the requested storage mode from the form (default value: 'raid1')
    storage_mode = "RS"
    print("Storage mode: %s" % storage_mode)

    # Reed Solomon code
    # Parse max_erasures (everything is a string in request.form, 
    # we need to convert to int manually), set default value to 1
    max_erasures = int(payload.get('max_erasures', 1))
    print("Max erasures: %d" % (max_erasures))
    
    # Store the files
    startTime = time.perf_counter()
    fragment_names, encoding_time = rs.store_file(data, max_erasures, send_task_socket, response_socket)
    endTime = time.perf_counter()

    ms = (endTime-startTime) * 1000

    # Save measurement on thread
    thread1 = threading.Thread(target=writeMeasurement("RedundancyMeasurements.txt", size, ms))
    thread1.start()
    thread2 = threading.Thread(target=writeMeasurement("EncodingMeasurements.txt", size, encoding_time))
    thread2.start()

    storage_details = {
        "coded_fragments": fragment_names,
        "max_erasures": max_erasures
    }

    # Insert the File record in the DB
    import json
    db = get_db()
    cursor = db.execute(
        "INSERT INTO `file`(`filename`, `size`, `content_type`, `storage_mode`, `storage_details`) VALUES (?,?,?,?,?)",
        (filename, size, content_type, storage_mode, json.dumps(storage_details))
    )
    db.commit()

    return make_response({"id": cursor.lastrowid }, 201)
#



@app.errorhandler(500)
def server_error(e):
    logging.exception("Internal error: %s", e)
    return make_response({"error": str(e)}, 500)


# Start the Flask app (must be after the endpoint functions) 
host_local_computer = "localhost" # Listen for connections on the local computer
host_local_network = "0.0.0.0" # Listen for connections on the local network
app.run(host=host_local_network if is_raspberry_pi() else host_local_computer, port=9000)
