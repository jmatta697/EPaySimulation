# this module is used to set up the database of card (account) holders

import sqlite3
from Cardholder import Cardholder

# establish connection with the database
conn = sqlite3.connect('Issuer_Cardholders_Data.db')
# define a 'cursor' for the database
c = conn.cursor()

# create a table to hold card holder information
c.execute("""CREATE TABLE cardholders (
            first text,
            last text,
            card_number text,
            exp_month text,
            exp_year text,
            cvv text,
            balance_amount float,
            pin_number text
            )""")

# define some card holder objects
cardholder_1 = Cardholder('Mary', 'Buckingham', '2345654349876543', '3', '2022', '123', 2345.67, '1234')
cardholder_2 = Cardholder('Sam', 'Smith', '2345654509812346', '4', '2023', '678', 345.67, '5678')
cardholder_3 = Cardholder('Bob', 'Bell', '5678654560980097', '3', '2022', '298', 765.67, '9012')
cardholder_4 = Cardholder('Joe', 'Mathew', '3456500098675542', '10', '2021', '345', 100.00, '2345')
cardholder_5 = Cardholder('Tony', 'Mathew', '3323000999876543', '2', '2021', '567', 200.50, '5678')

card_holder_list = [cardholder_1, cardholder_2, cardholder_3, cardholder_4, cardholder_5]
# insert all card holders into the card holder table
for ch in card_holder_list:
    c.execute("INSERT INTO cardholders VALUES (:first, :last, :card_number, :exp_month, :exp_year, :cvv, "
              ":balance_amount, :pin_number)", {'first': ch.first_name, 'last': ch.last_name,
                                                'card_number': ch.card_number,
                                                'exp_month': ch.exp_date_month, 'exp_year': ch.exp_date_year,
                                                'cvv': ch.cvv_number, 'balance_amount': ch.balance_amt,
                                                'pin_number': ch.pin_number})

conn.commit()
conn.close()
