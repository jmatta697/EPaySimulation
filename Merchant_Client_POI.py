import socket
import string
import sys
import RSA_Algorithm


def _set_up_socket(ip, port) -> socket.socket:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect socket to the port where the server is listening
    server_address = (ip, port)
    print(f'connecting to server {server_address[0]} on port {server_address[1]}')
    sock.connect(server_address)
    # return socket object
    return sock


def _send_receive_data(sock: socket.socket, data: bytes) -> str:
    try:
        # ----- Data going out to Server -----
        print(sys.stderr, f'POI sending to issuer >>> {data}')
        # send data into the socket (QR code string must be converted to a byte string)
        sock.sendall(data)

        # ----- Data coming back from Server -----
        # keep receiving until entire expected message is received
        # look for response by message length
        amount_received = 0
        # server response string
        server_response = b''
        amount_expected = len(data)
        # keep receiving until entire expected message is received
        while amount_received < amount_expected:
            data_segment = sock.recv(512)
            amount_received += len(data_segment)
            # build response string
            if data_segment:
                server_response += data_segment
            else:
                print('no more response data from server')
                break

    finally:
        print(sys.stderr, '** SEND_RECEIVE_COMPLETE **')

    return str(server_response)


# converts token bytes into a string and creates list where each element is a attribute in the token
def _itemize_token(token: str) -> [str]:
    # split token on '|' - strip first 'b' char off byte string
    token_list = token.split('|')
    print(token_list)
    return token_list


def _combine_encrypted_int_list(int_list: [int]) -> str:
    out_str = ''
    for integer in int_list:
        out_str += '|' + str(integer)
    out_str = out_str[1:-1]
    return out_str


def initiate_issuer_authorization(customer_data: bytes) -> str:
    # set up socket
    skt = _set_up_socket('localhost', 22567)

    # get RSA keys here - key_dict
    rsa_key_dict = RSA_Algorithm.generate_random_keys()
    # extract the public keys (n, e)
    n_public_key, e_public_key, d_private_key = rsa_key_dict['n'], rsa_key_dict['e'], rsa_key_dict['d']
    # build the public key transmission
    key_transmission_str = 'RSA_public_keys|' + str(n_public_key) + '|' + str(e_public_key)
    key_response = _send_receive_data(skt, key_transmission_str.encode())
    # print(key_response)
    server_key_list = _itemize_token(key_response)
    server_n_key = server_key_list[1]
    server_e_key = server_key_list[2]
    # encrypt customer_data using server public keys and this public key
    encrypted_customer_data_int_list = \
        RSA_Algorithm.rsa_encrypt(customer_data.decode(), d_private_key, n_public_key,
                                  int(server_e_key.translate(str.maketrans('', '', string.punctuation))),
                                  int(server_n_key.translate(str.maketrans('', '', string.punctuation))))
    # convert integer list into a string
    customer_data_str = _combine_encrypted_int_list(encrypted_customer_data_int_list)
    # print(customer_data_str)
    # send customer data to issuer server - this function will return a str with the response
    response = _send_receive_data(skt, customer_data_str.encode())

    skt.close()
    return response


