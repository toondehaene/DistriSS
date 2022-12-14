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
    proxy_address = "102"
    sender_address = "tcp://192.168.0."+proxy_address+":5557"
    receiver_address = "tcp://192.168.0."+proxy_address+":5555"
    fragment_request_address = "tcp://192.168.0."+proxy_address+":5559"
    fragment_response_address = "tcp://192.168.0."+proxy_address+":5558"
    delegate_response_address = "tcp://192.168.0."+proxy_address+":5554"
else:
    # On the local computer: use localhost
    sender_address = "tcp://*:5557"
    receiver_address = "tcp://*:5555"
    fragment_request_address = "tcp://*:5559"
    fragment_response_address = "tcp://*:5558"
    delegate_response_address = "tcp://*:5554"

context = zmq.Context()
# Socket to receive Store Chunk messages from the controller
proxy_receiver = context.socket(zmq.PULL)
proxy_receiver.bind(receiver_address)

proxy_sender = context.socket(zmq.PUSH)
proxy_sender.bind(sender_address)

fragment_get = context.socket(zmq.PUB)
fragment_get.bind(fragment_request_address)

fragment_response = context.socket(zmq.PULL)
fragment_response.bind(fragment_response_address)

delegate_response = context.socket(zmq.PUB)
delegate_response.bind(delegate_response_address)

# Use a Poller to monitor three sockets at the same time
poller = zmq.Poller()
poller.register(proxy_receiver, zmq.POLLIN)

while True:
    try:
        # Poll all sockets
        socks = dict(poller.poll())
    except KeyboardInterrupt:
        break
    pass

    # At this point one or multiple sockets may have received a message

    if proxy_receiver in socks:

        # Incoming message on the 'receiver' socket where we get tasks to store a chunk
        msg = proxy_receiver.recv_multipart()

        # Parse the Protobuf message from the first frame
        task = messages_pb2.fragment_request()
        task.ParseFromString(msg[0])
        is_store = task.is_store

        if(is_store):
            print("Proxy got save-fragment request")
            data = msg[1]

            proxy_sender.send_multipart([
                task.SerializeToString(),
                data
            ])

        else:
            print("Proxy got get-fragment request")
            taskToSend = messages_pb2.fragment_request()
            taskToSend.filename = task.filename
            fragment_get.send(
                taskToSend.SerializeToString()
            )

            result = fragment_response.recv_multipart()

            delegate_response.send_multipart([
                result[0],
                result[1]
            ])
            
