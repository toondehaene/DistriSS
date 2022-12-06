import messages_pb2
import math
import random

from utils import random_string

def store_file(file_data, send_task_socket, response_socket):
    """
    Implements storing a file with RAID 1 using 4 storage nodes.

    :param file_data: A bytearray that holds the file contents
    :param send_task_socket: A ZMQ PUSH socket to the storage nodes
    :param response_socket: A ZMQ PULL socket where the storage nodes respond.
    :return: A list of the random generated chunk names, e.g. (c1,c2), (c3,c4)
    """

    size = len(file_data)
    num = 1

    # RAID 1: cut the file in half and store both halves 2x
    # file_data_1 = file_data[:math.ceil(size/2.0)]
    # file_data_2 = file_data[math.ceil(size/2.0):]

    # Generate two random chunk names for each half
    file_data_names = [random_string(8) for i in range(num)]
    # file_data_2_names = [random_string(8), random_string(8)]
    print("Filenames: %s" % file_data_names)
    # print("Filenames for part 2: %s" % file_data_2_names)

    # Send 2 'store data' Protobuf requests with the first half and chunk names
    for name in file_data_names:
        task = messages_pb2.storedata_request()
        task.filename = name
        send_task_socket.send_multipart([
            task.SerializeToString(),
            file_data
        ])

    # Send 2 'store data' Protobuf requests with the second half and chunk names
    # for name in file_data_2_names:
    #     task = messages_pb2.storedata_request()
    #     task.filename = name
    #     send_task_socket.send_multipart([
    #         task.SerializeToString(),
    #         file_data_2
    #     ])

    # Wait until we receive 4 responses from the workers
    for task_nbr in range(num):
        resp = response_socket.recv_string()
        print('Received: %s' % resp)
    
    # Return the chunk names of each replica
    return file_data_names
#

def store_file_delegated(file_data, delegate_socket, response_socket, filenames):
    """
    Implements storing a file with RAID 1 using 4 storage nodes.

    :param file_data: A bytearray that holds the file contents
    :param send_task_socket: A ZMQ PUSH socket to the storage nodes
    :param response_socket: A ZMQ PULL socket where the storage nodes respond.
    :return: A list of the random generated chunk names, e.g. (c1,c2), (c3,c4)
    """

    size = len(file_data)
    num = 1

    # RAID 1: cut the file in half and store both halves 2x
    # file_data_1 = file_data[:math.ceil(size/2.0)]
    # file_data_2 = file_data[math.ceil(size/2.0):]

    # Generate a file name
    file_data_name = random_string(8)
    # file_data_2_names = [random_string(8), random_string(8)]
    print("Filename: %s", file_data_name)
    # print("Filenames for part 2: %s" % file_data_2_names)

    # Send 1 'store data' Protobuf requests with the file name
    
    task = messages_pb2.storedata_request()
    task.filename = str(filenames)    
    delegate_socket.send_multipart([
        task.SerializeToString(),
        file_data
    ])

    # Send 2 'store data' Protobuf requests with the second half and chunk names
    # for name in file_data_2_names:
    #     task = messages_pb2.storedata_request()
    #     task.filename = name
    #     send_task_socket.send_multipart([
    #         task.SerializeToString(),
    #         file_data_2
    #     ])

    # Wait until we receive 1 response from the worker
    for task_nbr in range(num):
        resp = response_socket.recv_string()
        print('Received: %s' % resp)
    
    # Return the chunk names of each replica
    return file_data_name
#

# TODO: write this
# Get a file by requesting on a bound socket where all nodes are connected on. 
# Each send() on this socket will target the next connected, wrapping around
# We want to replace the normal get_file() by this one because we don't want to
# use publish / subscibe to get files as they all have the same name and all nodes are the same
def individual_get(filename, bound_socket):
    task = messages_pb2.getdata_request()
    # individual_bound_socket send task 
    # listen for response on individual_response_socket
    # return the retrieved file
    return
#

def get_file(part1_filenames, part2_filenames, data_req_socket, response_socket):
    """
    Implements retrieving a file that is stored with RAID 1 using 4 storage nodes.

    :param part1_filenames: List of chunk names that store the first half
    :param part2_filenames: List of chunk names that store the second half
    :param data_req_socket: A ZMQ SUB socket to request chunks from the storage nodes
    :param response_socket: A ZMQ PULL socket where the storage nodes respond.
    :return: The original file contents
    """
    # Select one chunk of each half
    part1_filename = part1_filenames[random.randint(0, len(part1_filenames)-1)]
    part2_filename = part2_filenames[random.randint(0, len(part2_filenames)-1)]

    # Request both chunks in parallel
    task1 = messages_pb2.getdata_request()
    task1.filename = part1_filename
    data_req_socket.send(
        task1.SerializeToString()
    )
    task2 = messages_pb2.getdata_request()
    task2.filename = part2_filename
    data_req_socket.send(
        task2.SerializeToString()
    )

    # Receive both chunks and insert them to 
    file_data_parts = [None, None]
    for _ in range(2):
        result = response_socket.recv_multipart()
        # First frame: file name (string)
        filename_received = result[0].decode('utf-8')
        # Second frame: data
        chunk_data = result[1]

        print("Received %s" % filename_received)

        if filename_received == part1_filename:
            # The first part was received
            file_data_parts[0] = chunk_data
        else:
            # The second part was received
            file_data_parts[1] = chunk_data

    print("Both chunks received successfully")
    
    # Combine the parts and return
    file_data = file_data_parts[0] + file_data_parts[1]
    return file_data
#