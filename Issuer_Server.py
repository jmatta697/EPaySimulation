import random
import socket
import string
import sys
import time
import sqlite3


def run_server():
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
        print(f'OPEN connection to client {client_address}...')
        try:
            # receive the data in small chunks
            while True:
                # print('server tick')
                merchant_token = connection.recv(512)
                print(f'received >>> {merchant_token}')
                # if there is still data being received
                if merchant_token:
                    merchant_token_str = merchant_token.decode()

                    # split token on '|' - strip first 'b' char off byte string
                    token_element_list = str(merchant_token_str).split('|')
                    print(token_element_list)
                    # check with database...
                    # establish connection with the database
                    conn = sqlite3.connect('issuer_cardholders_data.db')
                    # define a 'cursor' for the database
                    c = conn.cursor()
                    # Query database to see if the merchant data matches any record in the database
                    c.execute("SELECT * FROM cardholders WHERE "
                              "first=:first AND "
                              "last=:last AND "
                              "card_number=:cc_num AND "
                              "exp_month=:exp_mth AND "
                              "exp_year=:exp_yr AND "
                              "cvv=:cc_cvv", {'first': token_element_list[0],
                                              'last': token_element_list[1],
                                              'cc_num': token_element_list[2],
                                              'exp_mth': token_element_list[3],
                                              'exp_yr': token_element_list[4],
                                              'cc_cvv': token_element_list[5]})

                    rand_bytes = generate_random_bytes(len(merchant_token))
                    if c.fetchone():
                        print('found a matching record')
                        # NOW... Match PIN
                        # PIN is token_element_list[6]
                        # embed success message into random char response
                        return_msg = 'OK_Record_Found' + rand_bytes[15:]

                    else:
                        print('Record not found')
                        return_msg = 'ERROR_No_Record' + rand_bytes[15:]
                    connection.sendall(return_msg.encode())
                    conn.commit()
                    conn.close()
                # when there is no more data to receive (reached the end of client data)
                else:
                    print(f'reached end of data from {client_address}')
                    break

            # DO STUFF HERE WITH CONVERTING THE MERCHANT TOKEN TO DICTIONARY AND CHECKING WITH DATA BASE
            # print(f'MERCHANT_TOKEN: {merchant_token}')
            # connection.sendall('OK_-_Transaction Successful'.encode())
            #
            # print('sending response back to client...')

        finally:
            print(f'CLOSE connection to client {client_address}...')
            # close and lean up the connection
            connection.close()



def generate_random_bytes(num_bytes: int) -> str:
    rand_bytes = ''
    for _ in range(num_bytes):
        # generate random byte
        rand_bytes += random.choice(string.printable)
    return rand_bytes


def main():
    run_server()


if __name__ == '__main__':
    main()
