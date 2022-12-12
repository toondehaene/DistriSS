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

#response_receiver = context.socket(zmq.PULL)
#response_receiver.connect(save_response_address)

# Socket to receive Store Chunk messages from the controller
#delegate = context.socket(zmq.PULL)
#delegate.connect(delegate_address)

# Socket to receive Get Chunk messages from the controller
#subscriber = context.socket(zmq.SUB)
#subscriber.connect(get_fragment_address)

# Receive every message (empty subscription)
#subscriber.setsockopt(zmq.SUBSCRIBE, b'')

# Socket to receive Repair request messages from the controller
#repair_subscriber = context.socket(zmq.SUB)
#repair_subscriber.connect(repair_subscriber_address)
# Receive messages destined for all nodes
#repair_subscriber.setsockopt(zmq.SUBSCRIBE, b'all_nodes')

# Subscription to individual messages goes here
# TO BE DONE
# Socket to send repair results to the controller
#repair_sender = context.socket(zmq.PUSH)
#repair_sender.connect(repair_sender_address)


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
        resp = receiver.recv_string()
        print('Received: %s' % resp)

        for i in range(3):
            sender.send_string("Distributing work")
        # print("Acting as delegate")
        # # Incoming message on the 'receiver' socket where we get tasks to store a chunk
        # msg = delegate.recv_multipart()
        # # Parse the Protobuf message from the first frame
        # task = messages_pb2.delegate_request()
        # task.ParseFromString(msg[0])
        # filenames = task.filenames
        # max_erasures = task.max_erasures
        # filedata = bytearray(msg[1])

        # print("Starting RS store")
        # print(max_erasures)
        # fragment_names, encoding_time = rs.store_file(filedata, max_erasures, sender, filenames = filenames)
        
        # print("RS DONE")
#
