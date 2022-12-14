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
    proxy_response_address = "tcp://localhost:5554"
    lead_response_address = "tcp://localhost:5551"

context = zmq.Context()
# Socket to receive Store Chunk messages from the controller
receiver = context.socket(zmq.PULL)
receiver.connect(delegate_address)

sender = context.socket(zmq.PUSH)
sender.connect(proxy_send_address)

proxy_response = context.socket(zmq.PULL)
proxy_response.connect(proxy_response_address)

lead_response = context.socket(zmq.PUSH)
lead_response.connect(lead_response_address)

poller = zmq.Poller()
poller.register(receiver, zmq.POLLIN)

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
        isEncoding = task.encoding
        filenames = task.filenames
        max_erasures = task.max_erasures

        if(isEncoding):
            print("Received encoding delegation")
            filedata = bytearray(msg[1])
            fragment_names, encoding_time, pure_enc_time = rs.store_file(filedata, max_erasures, sender, filenames = filenames)
        else:
            print("Received decoding delegation")
            file_size = task.file_size
            file_data, fulltime, decodetime = rs.get_file(
               filenames,
               max_erasures,
               file_size,
               sender,
               proxy_response
            )

            lead_response.send(
                file_data
            )



#
