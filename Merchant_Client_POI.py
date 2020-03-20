import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect socket to the port where the server is listening
server_address = ('localhost', 22567)
print(f'connecting to server {server_address[0]} on port {server_address[1]}')
sock.connect(server_address)

try:
    # send data
    QR_data = 'start|this is a test of sending QR code data - 98776543234567|8765|987|98743|0000000|end'
    print(sys.stderr, f'sending >>> {QR_data}')
    # send data into the socket (QR code string must be converted to a byte string)
    sock.sendall(QR_data.encode())

    # look for response by message length
    amount_received = 0
    amount_expected = len(QR_data)

    # keep receiving until entire expected message is received
    while amount_received < amount_expected:
        data_segment = sock.recv(16)
        amount_received += len(data_segment)
        print(sys.stderr, f'received {data_segment}')

finally:
    print(sys.stderr, '** closing socket **')
    sock.close()
