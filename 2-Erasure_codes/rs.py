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
import time

STORAGE_NODES_NUM = 4

RS_CAUCHY_COEFFS = [
    bytearray([253, 126, 255, 127]),
    bytearray([126, 253, 127, 255]),
    bytearray([255, 127, 253, 126]),
    bytearray([127, 255, 126, 253])
]

def delegate_get_file(coded_fragments, max_erasures, file_size,
             data_req_socket, response_socket):
    task = messages_pb2.delegate_request()
    task.max_erasures = max_erasures
    task.encoding = False
    task.file_size = file_size

    for name in coded_fragments:
        task.filenames.append(name)

    data_req_socket.send(
        task.SerializeToString()
    )

    result = response_socket.recv()

    return result

def delegate_store_file(file_data, max_erasures, socket):
    fragment_names = []

    for _ in range(STORAGE_NODES_NUM):      
        name = random_string(8)
        fragment_names.append(name)

    task = messages_pb2.delegate_request()
    task.max_erasures = max_erasures
    task.encoding = True

    for name in fragment_names:
        task.filenames.append(name)
    
    socket.send_multipart([
        task.SerializeToString(),
        file_data
    ])

    return fragment_names

def encode(file_data, max_erasures, filenames=[]):
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
    tasks = []
    datas = []
    
    # Generate one coded fragment for each Storage Node
    for i in range(STORAGE_NODES_NUM):
        # Select the next Reed Solomon coefficient vector 
        coefficients = RS_CAUCHY_COEFFS[i]

        # Generate a coded fragment with these coefficients 
        # (trim the coeffs to the actual length we need)
        encoder.encode_symbol(symbol, coefficients[:symbols])

        try:
            name = filenames[i]
            print(name)
        except:
            name = random_string(8)

        fragment_names.append(name)
    
        task = messages_pb2.fragment_request()
        task.filename = name
        task.is_store = True

        tasks.append(task.SerializeToString())
        datas.append(coefficients[:symbols] + bytearray(symbol))
    return tasks, datas, fragment_names

def store_file(file_data, max_erasures, send_task_socket, filenames=[]):
    t1 = time.perf_counter()
    tasks, data, fragmentnames = encode(file_data, max_erasures, filenames)
    t2 = time.perf_counter()

    for i in range(STORAGE_NODES_NUM):
        send_task_socket.send_multipart([
            tasks[i],
            data[i]
        ])
    t3 = time.perf_counter()

    fullEncodingTime = t3-t1
    pureEncodingTime = t2-t1

    return fragmentnames, fullEncodingTime, pureEncodingTime
#

def decode_file(symbols):
  
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

    return data_out
#


def get_file(coded_fragments, max_erasures, file_size,
             data_req_socket, response_socket):

    t1 = time.perf_counter()
    # We need 4-max_erasures fragments to reconstruct the file, select this many 
    # by randomly removing 'max_erasures' elements from the given chunk names. 
    fragnames = copy.deepcopy(coded_fragments)
    for i in range(max_erasures):
        fragnames.remove(random.choice(fragnames))
    
    # Request the coded fragments in parallel
    for name in fragnames:
        task = messages_pb2.fragment_request()
        task.filename = name
        task.is_store = False
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

    # Measure time to decode
    t2 = time.perf_counter()
    file_data = decode_file(symbols)
    t3 = time.perf_counter()

    fullDecodingTime = t3-t1
    pureDecodingTime = t3-t2
    return file_data[:file_size], fullDecodingTime, pureDecodingTime


