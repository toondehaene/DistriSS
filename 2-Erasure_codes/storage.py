"""
Aarhus University - Distributed Storage course - Lab 7

Storage Node
"""
import zmq
import messages_pb2

import sys
import os

from utils import random_string, write_file, is_raspberry_pi

# Read the folder name where chunks should be stored from the first program argument
# (or use the current folder if none was given)
data_folder = sys.argv[1] if len(sys.argv) > 1 else "./"
if data_folder != "./":
    # Try to create the folder  
    try:
        os.mkdir('./'+data_folder)
    except FileExistsError as _:
        # OK, the folder exists 
        pass
print("Data folder: %s" % data_folder)

# Check whether the node has an id. If it doesn't, generate one and save it to disk.
try:
    with open(data_folder+'/.id', "r") as id_file:
        node_id = id_file.read()
        print("ID read from file: %s" % node_id)

except FileNotFoundError:
    # This is OK, this must be the first time the node was started
    node_id = random_string(8)
    # Save it to file for the next start
    with open(data_folder+'/.id', "w") as id_file:
        id_file.write(node_id)
        print("New ID generated and saved to file: %s" % node_id)

if is_raspberry_pi():
    print("HEJ")
    # On the Raspberry Pi: ask the user to input the last segment of the server IP address
    server_address = input("Server address: 192.168.0.___ ")
    pull_task_address = "tcp://192.168.0."+server_address+":5557"
    get_fragment_address = "tcp://192.168.0."+server_address+":5559"
    send_fragment_address = "tcp://192.168.0."+server_address+":5558"
    save_response_address = "tcp://192.168.0."+server_address+":5560"
else:
    # On the local computer: use localhost
    pull_task_address = "tcp://localhost:5557"
    get_fragment_address = "tcp://localhost:5559"
    send_fragment_address = "tcp://localhost:5558"
    save_response_address = "tcp://localhost:5560"

context = zmq.Context()
# Socket to receive Store Chunk messages from the controller
receiver = context.socket(zmq.PULL)
receiver.connect(pull_task_address)

#Socket to receive Get Chunk messages from the controller
subscriber = context.socket(zmq.SUB)
subscriber.connect(get_fragment_address)

#Receive every message (empty subscription)
subscriber.setsockopt(zmq.SUBSCRIBE, b'')

sender = context.socket(zmq.PUSH)
sender.connect(send_fragment_address)

# Socket to send results to the controller
response_sender = context.socket(zmq.PUSH)
response_sender.connect(save_response_address)

# Use a Poller to monitor three sockets at the same time
poller = zmq.Poller()
poller.register(receiver, zmq.POLLIN)
poller.register(subscriber, zmq.POLLIN)

while True:
    try:
        # Poll all sockets
        socks = dict(poller.poll())
    except KeyboardInterrupt:
        break
    pass

    if receiver in socks:
        # Incoming message on the 'receiver' socket where we get tasks to store a chunk
        msg = receiver.recv_multipart()
        # Parse the Protobuf message from the first frame
        task = messages_pb2.fragment_request()
        task.ParseFromString(msg[0])

        data = msg[1]

        print('Chunk to save: %s, size: %d bytes' % (task.filename, len(data)))

        chunk_local_path = data_folder+'/'+task.filename
        write_file(data, chunk_local_path)
        print("Chunk saved to %s" % chunk_local_path)
        
        response_sender.send_string("Fragment saved")


    if subscriber in socks:
        # Incoming message on the 'subscriber' socket where we get retrieve requests
        msg = subscriber.recv()
        
        # Parse the Protobuf message from the first frame
        task = messages_pb2.fragment_request()
        task.ParseFromString(msg)

        filename = task.filename
        print("Data chunk request: %s" % filename)

        # Try to load the requested file from the local file system,
        # send response only if found
        try:
            with open(data_folder+'/'+filename, "rb") as in_file:
                print("Found chunk %s, sending it back" % filename)

                sender.send_multipart([
                    bytes(filename, 'utf-8'),
                    in_file.read()
                ])
        except FileNotFoundError:
            # This is OK here
            pass
#
