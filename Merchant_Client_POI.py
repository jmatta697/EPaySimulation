import socket
import sys


def _set_up_socket(ip, port) -> socket.socket:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect socket to the port where the server is listening
    server_address = (ip, port)
    print(f'connecting to server {server_address[0]} on port {server_address[1]}')
    sock.connect(server_address)
    # return socket object
    return sock


def _send_receive_data(sock: socket.socket, customer_data: bytes) -> str:
    try:
        print(sys.stderr, f'POI sending to issuer >>> {customer_data}')
        # send data into the socket (QR code string must be converted to a byte string)
        sock.sendall(customer_data)

        # ----- Data coming back -----
        # look for response by message length
        amount_received = 0
        # server response string
        server_response = b''
        amount_expected = len(customer_data)
        # keep receiving until entire expected message is received
        while amount_received < amount_expected:
            data_segment = sock.recv(16)
            amount_received += len(data_segment)
            # build response string
            server_response += data_segment
            # print(sys.stderr, f'received {data_segment}')
    finally:
        print(sys.stderr, '** closing socket **')
        sock.close()

    return str(server_response)


def initiate_issuer_authorization(customer_data: bytes) -> str:
    skt = _set_up_socket('localhost', 22567)
    # send data to issuer server - this function will return a str with the response
    response = _send_receive_data(skt, customer_data)
    return response
