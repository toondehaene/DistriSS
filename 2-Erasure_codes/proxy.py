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
    # On the local computer: use localhost
    #delegate_address = "tcp://localhost:5556"
    sender_address = "tcp://*:5557"
    receiver_address = "tcp://*:5555"
    #repair_subscriber_address = "tcp://localhost:5560"
    #repair_sender_address = "tcp://localhost:5561"

context = zmq.Context()
# Socket to receive Store Chunk messages from the controller
proxy_receiver = context.socket(zmq.PULL)
proxy_receiver.bind(receiver_address)

proxy_sender = context.socket(zmq.PUSH)
proxy_sender.bind(sender_address)

# Use a Poller to monitor three sockets at the same time
poller = zmq.Poller()
poller.register(proxy_receiver, zmq.POLLIN)
#poller.register(subscriber, zmq.POLLIN)
#poller.register(delegate, zmq.POLLIN)
#poller.register(repair_subscriber, zmq.POLLIN


while True:
    try:
        # Poll all sockets
        socks = dict(poller.poll())
    except KeyboardInterrupt:
        break
    pass

    # At this point one or multiple sockets may have received a message

    if proxy_receiver in socks:
        resp = proxy_receiver.recv_string()
        print('Received: %s' % resp)

        proxy_sender.send_string("Distributing task")

        #print("Received msg at proxy subscriber")
        #proxy_sender.send_string("Publishing task from proxy")
        #print("Published message at proxy publisher")
