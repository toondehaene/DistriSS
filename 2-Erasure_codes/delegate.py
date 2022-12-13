"""
Aarhus University - Distributed Storage course - Lab 7

Storage Node
"""
import zmq
import messages_pb2
import rs

import sys
import os
import random
import string

from utils import random_string, write_file, is_raspberry_pi

if is_raspberry_pi():
    print("HEJ")
    # On the Raspberry Pi: ask the user to input the last segment of the server IP address
    #server_address = input("Server address: 192.168.0.___ ")
    #delegate_address = "tcp://192.168.0."+server_address+":5556"
    #pull_address = "tcp://192.168.0."+server_address+":5557"
    #sender_address = "tcp://192.168.0."+server_address+":5558"
    #subscriber_address = "tcp://192.168.0."+server_address+":5559"
    #repair_subscriber_address = "tcp://192.168.0."+server_address+":5560"
    #repair_sender_address = "tcp://192.168.0."+server_address+":5561"
else:
    delegate_address = "tcp://localhost:5556"
    proxy_send_address = "tcp://localhost:5555"
    #repair_subscriber_address = "tcp://localhost:5560"
    #repair_sender_address = "tcp://localhost:5561"

context = zmq.Context()
# Socket to receive Store Chunk messages from the controller
receiver = context.socket(zmq.PULL)
receiver.connect(delegate_address)

sender = context.socket(zmq.PUSH)
sender.connect(proxy_send_address)

#print("Listening on "+ save_fragment_address)

# Socket to send results to the controller
#response_sender = context.socket(zmq.PUSH)
#response_sender.connect(save_response_address)

# Use a Poller to monitor three sockets at the same time
poller = zmq.Poller()
poller.register(receiver, zmq.POLLIN)
#poller.register(subscriber, zmq.POLLIN)
#poller.register(delegate, zmq.POLLIN)
#poller.register(repair_subscriber, zmq.POLLIN

print("Starting to listen to be a delegate")

while True:
    try:
        # Poll all sockets
        socks = dict(poller.poll())
    except KeyboardInterrupt:
        break
    pass

    # At this point one or multiple sockets may have received a message

    if receiver in socks:

        msg = receiver.recv_multipart()

        task = messages_pb2.delegate_request()
        task.ParseFromString(msg[0])
        filenames = task.filenames
        max_erasures = task.max_erasures
        print(filenames)
        filedata = bytearray(msg[1])

        print("Starting RS store")
        fragment_names, encoding_time, pure_enc_time = rs.store_file(filedata, max_erasures, sender, filenames = filenames)
        print("Done sending to proxy")
        
#
