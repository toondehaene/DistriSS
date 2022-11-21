from flask import Flask, make_response, g, request, send_file
import sqlite3
import base64
import random
import string
import logging

import zmq # For ZMQ
import time # For waiting a second for ZMQ connections
import math # For cutting the file in half
import messages_pb2 # Generated Protobuf messages
import io # For sending binary data in a HTTP response
import logging

# from apscheduler.schedulers.background import BackgroundScheduler # automated repair
import atexit # unregister scheduler at app exit

import raid1
import reedsolomon
import rlnc

from utils import is_raspberry_pi

# Instantiate the Flask app (must be before the endpoint functions)
app = Flask(__name__)


@app.route('/test')
def hello():
    payload = request.get_json()
    if payload == None:
            print("this is actually none")
    return make_response({'message': 'Hello World!'})


# Start the Flask app (must be after the endpoint functions) 
host_local_computer = "localhost" # Listen for connections on the local computer
host_local_network = "0.0.0.0" # Listen for connections on the local network
app.run(host=host_local_network if is_raspberry_pi() else host_local_computer, port=9000)
