"""
Aarhus University - Distributed Storage course - Lab 7

Reed-Solomon coder
"""
import kodo
import math
import random
import copy # for deepcopy
from utils import random_string
import messages_pb2
import json
import time

STORAGE_NODES_NUM = 1

RS_CAUCHY_COEFFS = [
    bytearray([253, 126, 255, 127]),
    bytearray([126, 253, 127, 255]),
    bytearray([255, 127, 253, 126]),
    bytearray([127, 255, 126, 253])
]

def delegate_filestoring(file_data, max_erasures, socket):
    fragment_names = []
    for _ in range(STORAGE_NODES_NUM):      
        name = random_string(8)
        fragment_names.append(name)

    task = messages_pb2.delegate_request()
    task.max_erasures = max_erasures

    for name in fragment_names:
        task.filenames.append(name)
    
    socket.send_multipart([
        task.SerializeToString(),
        file_data
    ])

    return fragment_names

def store_file(file_data, max_erasures, send_task_socket, filenames=[]):
    # Measure time tp decode
    startTime = time.perf_counter()
   
    # Make sure we can realize max_erasures with 4 storage nodes
    assert(max_erasures >= 0)
    assert(max_erasures < STORAGE_NODES_NUM)

    # How many coded fragments (=symbols) will be required to reconstruct the encoded data. 
    symbols = STORAGE_NODES_NUM - max_erasures
    # The size of one coded fragment (total size/number of symbols, rounded up)
    symbol_size = math.ceil(len(file_data)/symbols)
    # Kodo RLNC encoder using 2^8 finite field
    encoder = kodo.block.Encoder(kodo.FiniteField.binary8)
    encoder.configure(symbols, symbol_size)
    encoder.set_symbols_storage(file_data)
    symbol = bytearray(encoder.symbol_bytes)

    fragment_names = []

    # Generate one coded fragment for each Storage Node
    for i in range(STORAGE_NODES_NUM):
        # Select the next Reed Solomon coefficient vector 
        coefficients = RS_CAUCHY_COEFFS[i]

        # Generate a coded fragment with these coefficients 
        # (trim the coeffs to the actual length we need)
        encoder.encode_symbol(symbol, coefficients[:symbols])

        # Generate a random name for it and save
        try:
            name = filenames[i]
            print(name)
        except:
            name = random_string(8)
            print("RANDOM NAME")

        fragment_names.append(name)
        
        # Send a Protobuf STORE DATA request to the Storage Nodes
        task = messages_pb2.storedata_request()
        task.filename = name

        send_task_socket.send_multipart([
            task.SerializeToString(),
            coefficients[:symbols] + bytearray(symbol)
        ])

    endTime = time.perf_counter()

    ms_encoding = (endTime-startTime) * 1000
    
    #print("Waiting for response.")
    # Wait until we receive a response for every fragment
    #for task_nbr in range(STORAGE_NODES_NUM):
        #print("Started response loop")
        #resp = response_socket.recv_string()
        #print('Received: %s' % resp)

    return fragment_names, ms_encoding
#


def decode_file(symbols):
    """
    Decode a file using Reed Solomon decoder and the provided coded symbols.
    The number of symbols must be the same as STORAGE_NODES_NUM - max_erasures.

    :param symbols: coded symbols that contain both the coefficients and symbol data
    :return: the decoded file data
    """

    # Reconstruct the original data with a decoder
    symbols_num = len(symbols)
    symbol_size = len(symbols[0]['data']) - symbols_num #subtract the coefficients' size
    decoder = kodo.block.Decoder(kodo.FiniteField.binary8)
    decoder.configure(symbols_num, symbol_size)
    data_out = bytearray(decoder.block_bytes)
    decoder.set_symbols_storage(data_out)

    for symbol in symbols:
        # Separate the coefficients from the symbol data
        coefficients = symbol['data'][:symbols_num]
        symbol_data = symbol['data'][symbols_num:]
       
        # Feed it to the decoder
        decoder.decode_symbol(symbol_data, coefficients)

    # Make sure the decoder successfully reconstructed the file
    assert(decoder.is_complete())
    print("File decoded successfully")

    return data_out
#


def get_file(coded_fragments, max_erasures, file_size,
             data_req_socket, response_socket):
    """
    Implements retrieving a file that is stored with Reed Solomon erasure coding

    :param coded_fragments: Names of the coded fragments
    :param max_erasures: Max erasures setting that was used when storing the file
    :param file_size: The original data size. 
    :param data_req_socket: A ZMQ SUB socket to request chunks from the storage nodes
    :param response_socket: A ZMQ PULL socket where the storage nodes respond.
    :return: A list of the random generated chunk names, e.g. (c1,c2), (c3,c4)
    """
    
    # We need 4-max_erasures fragments to reconstruct the file, select this many 
    # by randomly removing 'max_erasures' elements from the given chunk names. 
    fragnames = copy.deepcopy(coded_fragments)
    for i in range(max_erasures):
        fragnames.remove(random.choice(fragnames))
    
    # Request the coded fragments in parallel
    for name in fragnames:
        task = messages_pb2.getdata_request()
        task.filename = name
        data_req_socket.send(
            task.SerializeToString()
            )

    # Receive all chunks and insert them into the symbols array
    symbols = []
    for _ in range(len(fragnames)):
        result = response_socket.recv_multipart()
        # In this case we don't care about the received name, just use the 
        # data from the second frame
        symbols.append({
            "chunkname": result[0].decode('utf-8'), 
            "data": bytearray(result[1])
        })
    print("All coded fragments received successfully")

    # Measure time tp decode
    startTime = time.perf_counter()
    file_data = decode_file(symbols)
    endTime = time.perf_counter()

    ms_decoding = (endTime-startTime) * 1000

    return file_data[:file_size], ms_decoding
#

# get_file_for_repair goes here
# TO BE DONE


# Repair process implementation goes here
# TO BE DONE
