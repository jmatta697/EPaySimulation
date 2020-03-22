import random
import socket
import string
import sys
import sqlite3
from typing import Any


def run_server():
    # setup socket and listen
    sock = _create_socket('localhost', 22567)
    while True:
        # wait for a connection
        print('Waiting for a connection...')
        connection, client_address = sock.accept()
        print(f'OPEN connection to client {client_address}...')
        try:
            while True:
                # print('server tick')
                # receive the data in 512 chunks
                merchant_token = connection.recv(512)
                print(f'server received merchant token from POI >>> {merchant_token}')

                # assemble token in to string list with each element representing a customer information attribute
                token_element_list = _itemize_poi_token(merchant_token)
                # if there is still data being received
                if merchant_token:
                    # check with database...
                    db_conn, c = _establish_database_connection('issuer_cardholders_data.db')
                    # Query database to see if the merchant data matches any record in the database
                    return_msg, db_record = _check_database_for_record(c, merchant_token, token_element_list)
                    # DEBUG print
                    print(return_msg, db_record)
                    # a database record is found.. check PIN
                    if db_record:
                        # now check PIN - PIN is token_element_list[6]
                        return_msg = _check_pin(token_element_list[6], db_record[7], return_msg)
                        # now process payment - if possible and valid PIN
                        if return_msg[16:27] == 'VALID___PIN':
                            print('we are processing payment...')
                            # check if there are sufficient funds in the customers account
                            if _sufficient_funds(token_element_list[7], db_record[6]):
                                print('there is sufficient funds')
                                return_msg = _update_message_transaction_complete(return_msg)
                                _process_payment(c, db_record, token_element_list)
                            else:
                                print('not enough funds!')
                                return_msg = _update_message_insufficient_funds(return_msg)

                    connection.sendall(return_msg.encode())
                    db_conn.commit()
                    db_conn.close()
                # when there is no more data to receive (reached the end of client data)
                else:
                    # print(f'reached end of data from {client_address}')
                    break
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


def _create_socket(ip: str, port: int) -> socket.socket:
    # create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to the port
    server_address = (ip, port)
    print(sys.stderr, f'\nstarting server on {server_address[0]}: port {server_address[1]}')
    sock.bind(server_address)
    # listen for incoming connection
    sock.listen(1)
    return sock


# converts the POI token bytes into a string and creates list where each element is a attribute in the token
def _itemize_poi_token(raw_token: bytes) -> [str]:
    merchant_token_str = raw_token.decode()
    # split token on '|' - strip first 'b' char off byte string
    token_list = str(merchant_token_str).split('|')
    print(token_list)
    return token_list


def _establish_database_connection(database_name: str) -> (sqlite3.Connection, sqlite3.Cursor):
    # establish connection with the database
    conn = sqlite3.connect(database_name)
    # define a 'cursor' for the database
    c = conn.cursor()
    return conn, c


def _check_database_for_record(c: sqlite3.Cursor, raw_token: bytes, customer_item_list: [str]) -> (str, Any):
    # use select statement to find if the customer information matches a record in the database
    c.execute("""SELECT * FROM cardholders WHERE 
              first=:first AND 
              last=:last AND 
              card_number=:cc_num AND
              exp_month=:exp_mth AND 
              exp_year=:exp_yr AND 
              cvv=:cc_cvv""", {'first': customer_item_list[0],
                               'last': customer_item_list[1],
                               'cc_num': customer_item_list[2],
                               'exp_mth': customer_item_list[3],
                               'exp_yr': customer_item_list[4],
                               'cc_cvv': customer_item_list[5]})
    # generate random bytes equal in amount to the raw number of bytes received from POI
    rand_bytes = generate_random_bytes(len(raw_token))
    # if record is found fetchone will return something
    db_record = c.fetchone()
    if db_record:
        print('POI token matched a record')
        # embed success message into random char response
        return_msg = 'OK_Record_Found' + rand_bytes[15:]
    # no matching records result in fetchone returning NONE
    else:
        print('Record not found')
        return_msg = 'ERROR_No_Record' + rand_bytes[15:]
    return return_msg, db_record


def _check_pin(incoming_pin: str, record_pin: str, return_message: str) -> str:
    if incoming_pin == record_pin:
        print('PIN entered at POI is VALID')
        update_msg = return_message[:15] + '|VALID___PIN|' + return_message[28:]
    else:
        print('PIN entered at POI is INVALID')
        update_msg = return_message[:15] + '|INVALID_PIN|' + return_message[28:]
    return update_msg


def _sufficient_funds(payment_request: str, record_balance: float) -> bool:
    payment_amount_float = float(payment_request)
    if record_balance - payment_amount_float < 0:
        return False
    return True


def _process_payment(c: sqlite3.Cursor, db_record, customer_item_list: [str]):
    # do math to get new balance (amount in db_rec[6] - customer_item_list[7]
    new_balance = db_record[6] - float(customer_item_list[7])
    # round new_balance to closest cent
    new_balance = round(new_balance, 2)
    print(new_balance)
    # update customer account balance in database
    c.execute("""UPDATE cardholders 
              SET balance_amount=:nb WHERE 
              first=:first AND 
              last=:last AND 
              card_number=:cc_num AND 
              exp_month=:exp_mth AND 
              exp_year=:exp_yr AND 
              cvv=:cc_cvv""", {'first': customer_item_list[0],
                               'last': customer_item_list[1],
                               'cc_num': customer_item_list[2],
                               'exp_mth': customer_item_list[3],
                               'exp_yr': customer_item_list[4],
                               'cc_cvv': customer_item_list[5],
                               'nb': new_balance})


def _update_message_insufficient_funds(msg: str) -> str:
    # if more rand chars are available add them
    ret_msg = msg[:28] + 'INSUF_FUND|' + msg[39:]
    print(ret_msg)
    return ret_msg


def _update_message_transaction_complete(msg: str) -> str:
    # if more rand chars are available add them
    ret_msg = msg[:28] + 'TRANS_CPLT|' + msg[39:]
    print(ret_msg)
    return ret_msg




def main():
    run_server()


if __name__ == '__main__':
    main()
