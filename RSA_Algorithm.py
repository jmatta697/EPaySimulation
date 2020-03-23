# Author: Joe Matta
# November 2018
import random
from typing import Dict


# https://stackoverflow.com/questions/15285534/isprime-function-for-python-language
def _is_prime(test_num) -> bool:
    if test_num == 2 or test_num == 3:
        return True
    if test_num % 2 == 0 or test_num < 2:
        return False
    for i in range(3, int(test_num ** 0.5) + 1, 2):  # only odd numbers
        if test_num % i == 0:
            return False
    return True


def _generate_prime_num_list(min_range: int, max_range: int) -> [int]:
    prime_numbers = [i for i in range(min_range, max_range) if _is_prime(i)]
    return prime_numbers


# choose two prime numbers
def _choose_two_prime_numbers(prime_list: [int]) -> (int, int):
    random.shuffle(prime_list)
    first_prime = prime_list.pop()
    second_prime = prime_list.pop()
    return first_prime, second_prime


def _gcd(a, b):
    if b == 0:
        return a
    else:
        return _gcd(b, a % b)


def _get_e(phi_n_value: int) -> int:
    # choose random number from 10 to phi_n_value//128
    rand_e_iter_min = random.randrange(10, phi_n_value//32)
    for e_iter in range(rand_e_iter_min, phi_n_value):
        if _gcd(e_iter, phi_n_value) == 1:
            return e_iter


# https://gist.github.com/JekaDeka/c9b0f5da16625e3c7bd1033356354579
def _multiplicative_inverse(a, b):
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a  # Remember original a/b to remove
    ob = b  # negative values from return results
    while b != 0:
        q_val = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q_val * x)), x)
        (y, ly) = ((ly - (q_val * y)), y)
    if lx < 0:
        lx += ob  # If neg wrap modulo original b
    if ly < 0:
        ly += oa  # If neg wrap modulo original a
    return lx


def generate_random_keys() -> Dict[str, int]:
    key_dictionary = {}
    # generate prime list to choose from
    prime_num_list = _generate_prime_num_list(160, 180)
    # random choose p and q
    p, q = _choose_two_prime_numbers(prime_num_list)
    # determine n (public key)
    n = p*q
    # add n (public key) to dictionary
    key_dictionary['n'] = n
    # determine phi(n)
    phi_n = (p-1)*(q-1)
    # choose e (public key)
    e = _get_e(phi_n)
    # add e (public key) to dictionary
    key_dictionary['e'] = e
    # compute unique number d (private key)
    d = _multiplicative_inverse(e, phi_n)
    # add d (private key) to dictionary
    key_dictionary['d'] = d
    print(f'\np: {p}\nq: {q}\nn: {n}\nphi_n: {phi_n}\ne: {e}\nd: {d}\n')
    return key_dictionary


def rsa_encrypt(plain_text: str, my_private_d: int, my_public_n: int, outside_e: int, outside_n: int) -> [int]:
    cypher_str = []
    for char in plain_text:
        char_ascii_value = ord(char)
        encrypted_char = (((char_ascii_value**my_private_d) % my_public_n) ** outside_e) % outside_n
        cypher_str.append(encrypted_char)
    return cypher_str


def rsa_decrypt(cypher_text: [int], my_private_d: int, my_public_n: int, outside_e: int, outside_n: int) -> [int]:
    plain_text_ascii = []
    for cypher_char in cypher_text:
        ascii_value = (((cypher_char**my_private_d) % my_public_n)**outside_e) % outside_n
        plain_text_ascii.append(ascii_value)
    return plain_text_ascii


def convert_ascii_to_string(ascii_list: [int]) -> str:
    return ''.join(chr(ascii_value) for ascii_value in ascii_list)


# ------ TEST CASE BELOW -------

# my-client
# p: 59
# q: 71
# n: 4189
# phi_n: 4060
# e: 31
# d: 131

# outside-server
# p: 61
# q: 89
# n: 5429
# phi_n: 5280
# e: 29
# d: 2549

# client encrypts massage
# encrypted_text = rsa_encrypt('Gi Joe', 131, 4189, 29, 5429)
# print(encrypted_text)

# server decrypts message
# decrypted_text = rsa_decrypt(encrypted_text, 2549, 5429, 31, 4189)
# print(decrypted_text)
# decrypted_plain_text = convert_ascii_to_string(decrypted_text)
# print(decrypted_plain_text)
