"""
Aarhus University - Distributed Storage course - Lab 7

Storage Node
"""
import zmq
import messages_pb2
import rs

from utils import is_raspberry_pi

if is_raspberry_pi():
    # On the Raspberry Pi: ask the user to input the last segment of the server IP address
    proxy_address = "102"
    sender_address = "tcp://192.168.0."+proxy_address+":5557"
    receiver_save_address = "tcp://192.168.0."+proxy_address+":5555"
    receiver_get_address = "tcp://192.168.0."+proxy_address+":5550"
    fragment_request_address = "tcp://192.168.0."+proxy_address+":5559"
    fragment_response_address = "tcp://192.168.0."+proxy_address+":5558"
    delegate_response_address = "tcp://192.168.0."+proxy_address+":5554"
else:
    # On the local computer: use localhost
    sender_address = "tcp://*:5557"
    receiver_save_address = "tcp://*:5555"
    receiver_get_address = "tcp://*:5550"
    fragment_request_address = "tcp://*:5559"
    fragment_response_address = "tcp://*:5558"
    delegate_response_address = "tcp://*:5554"

context = zmq.Context()
# Socket to receive Store Chunk messages from the controller
proxy_receiver_save = context.socket(zmq.PULL)
proxy_receiver_save.bind(receiver_save_address)

proxy_receiver_get = context.socket(zmq.PULL)
proxy_receiver_get.bind(receiver_get_address)

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
poller.register(proxy_receiver_save, zmq.POLLIN)
poller.register(proxy_receiver_get, zmq.POLLIN)

print("Proxy started")

while True:
    try:
        # Poll all sockets
        socks = dict(poller.poll())
    except KeyboardInterrupt:
        break
    pass

    # At this point one or multiple sockets may have received a message

    if proxy_receiver_save in socks:

        # Incoming message on the 'receiver' socket where we get tasks to store a chunk
        msg = proxy_receiver_save.recv_multipart()

        # Parse the Protobuf message from the first frame
        task = messages_pb2.fragment_request()
        task.ParseFromString(msg[0])

        print("Proxy got save-fragment request")
        data = msg[1]

        proxy_sender.send_multipart([
            task.SerializeToString(),
            data
        ])

    if proxy_receiver_get in socks:
        msg = proxy_receiver_get.recv()
        task = messages_pb2.get_fragments_request()
        task.ParseFromString(msg)

        filenames = task.filenames
        max_erasures = task.max_erasures
        request_id = task.request_id

        chunknames, data = rs.get_fragments(filenames, max_erasures, fragment_get, fragment_response)
        print("Got all fragments, sending back to delegate")
        responseTask = messages_pb2.fragments_reponse()
        responseTask.request_id = request_id
        
        for i in range(len(chunknames)):
            responseTask.filenames.append(chunknames[i])
            responseTask.chunks.append(data[i])

        delegate_response.send(
            responseTask.SerializeToString()
        )
            
