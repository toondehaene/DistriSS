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

from utils import is_raspberry_pi

if is_raspberry_pi():
    # On the Raspberry Pi: ask the user to input the last segment of the server IP address
    server_address = "101"
    proxy_address = "102"
    delegate_address = "tcp://192.168.0."+server_address+":5556"
    proxy_send_save_address = "tcp://192.168.0."+proxy_address+":5555"
    proxy_send_get_address = "tcp://192.168.0."+proxy_address+":5550"
    proxy_response_address = "tcp://192.168.0."+proxy_address+":5554"
    lead_response_address = "tcp://192.168.0."+server_address+":5551"
else:
    delegate_address = "tcp://localhost:5556"
    proxy_send_save_address = "tcp://localhost:5555"
    proxy_send_get_address = "tcp://localhost:5550"
    proxy_response_address = "tcp://localhost:5554"
    lead_response_address = "tcp://localhost:5551"

context = zmq.Context()
# Socket to receive Store Chunk messages from the controller
receiver = context.socket(zmq.PULL)
receiver.connect(delegate_address)

sender_save = context.socket(zmq.PUSH)
sender_save.connect(proxy_send_save_address)

sender_get = context.socket(zmq.PUSH)
sender_get.connect(proxy_send_get_address)

proxy_response = context.socket(zmq.SUB)
proxy_response.connect(proxy_response_address)
proxy_response.setsockopt(zmq.SUBSCRIBE, b'')

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
            fragment_names, encoding_time, pure_enc_time = rs.store_file(filedata, max_erasures, sender_save, filenames = filenames)
        else:
            print("Received decoding delegation")
            file_size = task.file_size

            taskToSend = messages_pb2.get_fragments_request()

            for name in filenames:
                taskToSend.filenames.append(name)

            taskToSend.max_erasures = max_erasures

            sender_get.send(
                taskToSend.SerializeToString()
            )

            msg = proxy_response.recv()
            print("Got shit back from proxy")
            task = messages_pb2.fragments_reponse()
            task.ParseFromString(msg)

            names = task.filenames
            data = task.chunks

            symbols = []
            for i in range(len(names)):
                symbols.append({
                    "chunkname": names[i], 
                    "data": bytearray(data[i])
                })

            file_data = rs.decode_file(symbols)
            file_data = file_data[:file_size]

            print("Sending back to lead")
            lead_response.send(
                file_data
            )



#
