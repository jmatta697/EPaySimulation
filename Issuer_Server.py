import socket
import sys

# create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the port
server_address = ('localhost', 22567)
print(sys.stderr, f'\nstarting server on {server_address[0]}: port {server_address[1]}')
sock.bind(server_address)

# listen for incoming connection
sock.listen(1)

while True:
    # wait for a connection
    print('Waiting for a connection...')
    connection, client_address = sock.accept()
    try:
        print(f'trying to connect with {client_address}...')
        # receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print(f'received >>> {data}')
            # if there is still data being received
            if data:
                print('sending data back to client...')
                connection.sendall(data)
            # when there is no more data to receive (reached the end of client data)
            else:
                print(f'reached end of data from {client_address}')
                break
    finally:
        # close and lean up the connection
        connection.close()
