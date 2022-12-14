from flask import Flask, make_response, g, request, send_file
import sqlite3
import logging

import zmq # For ZMQ
import time # For waiting a second for ZMQ connections
import io # For sending binary data in a HTTP response
import logging
import rs
import utils
import sys
import json

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

delegate = sys.argv[1].lower() == 'true'

context = zmq.Context()

if(delegate):
    print("Starting API with delegation")
    delegate_request_socket = context.socket(zmq.PUSH)
    delegate_request_socket.bind("tcp://*:5556")
    
    delegate_response_socket = context.socket(zmq.SUB)
    delegate_response_socket.bind("tcp://*:5551")
    delegate_response_socket.setsockopt(zmq.SUBSCRIBE, b'')
else:
    print("Starting regular API")
    save_file_socket = context.socket(zmq.PUSH)
    save_file_socket.bind("tcp://*:5557")

    data_response_socket = context.socket(zmq.PULL)
    data_response_socket.bind("tcp://*:5558")

    data_request_socket = context.socket(zmq.PUB)
    data_request_socket.bind("tcp://*:5559")

save_done_socket = context.socket(zmq.PULL)
save_done_socket.bind("tcp://*:5560")
 
time.sleep(1)

app = Flask(__name__)
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
    storage_details = json.loads(f['storage_details'])

    coded_fragments = storage_details['coded_fragments']
    max_erasures = storage_details['max_erasures']
    fulltime = -1
    decodetime = -1

    if(delegate):
        file_data = rs.delegate_get_file(
            coded_fragments,
            max_erasures,
            f['size'],
            delegate_request_socket,
            delegate_response_socket
        )
    else:
        file_data, fulltime, decodetime = rs.get_file(
            coded_fragments,
            max_erasures,
            f['size'],
            data_request_socket, 
            data_response_socket
        )

    response = send_file(io.BytesIO(file_data), mimetype=f['content_type'])
    response.headers['fullDecTime'] = fulltime
    response.headers['pureDecTime'] = decodetime

    return response
#

@app.route('/files_mp', methods=['POST'])
def add_files_multipart():
    t1 = time.time()
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
    
    storage_mode = "RS"

    max_erasures = int(payload.get('max_erasures', 1))
    fullTime = -1
    encodingTime = -1

    if(delegate):
        fragment_names = rs.delegate_store_file(data, max_erasures, delegate_request_socket)
    else:
        fragment_names, fullTime, encodingTime = rs.store_file(data, max_erasures, save_file_socket)

    storage_details = {
        "coded_fragments": fragment_names,
        "max_erasures": max_erasures
    }

    t2 = time.time() # TODO: Should this be below database?

    # Insert the File record in the DB
    import json
    db = get_db()
    cursor = db.execute(
        "INSERT INTO `file`(`filename`, `size`, `content_type`, `storage_mode`, `storage_details`) VALUES (?,?,?,?,?)",
        (filename, size, content_type, storage_mode, json.dumps(storage_details))
    )
    db.commit()

    # Wait until we receive a response for every fragment
    print("Started response loop")
    for _ in range(rs.STORAGE_NODES_NUM):
        resp = save_done_socket.recv_string()
        print('Received: %s' % resp)

    t3 = time.time()

    return make_response({"id": cursor.lastrowid, "lead_done": t2-t1, "last_done": t3-t1, "pure_enc": encodingTime, "full_enc": fullTime }, 201)
#

@app.errorhandler(500)
def server_error(e):
    logging.exception("Internal error: %s", e)
    return make_response({"error": str(e)}, 500)

# Start the Flask app (must be after the endpoint functions) 
host_local_computer = "localhost" # Listen for connections on the local computer
host_local_network = "0.0.0.0" # Listen for connections on the local network
app.run(host=host_local_network if utils.is_raspberry_pi() else host_local_computer, port=9000)
