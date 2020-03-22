# Author: Joe Matta
# November 2018
import random


# https://stackoverflow.com/questions/15285534/isprime-function-for-python-language
def is_prime(test_num) -> bool:
    if test_num == 2 or test_num == 3:
        return True
    if test_num % 2 == 0 or test_num < 2:
        return False
    for i in range(3, int(test_num ** 0.5) + 1, 2):  # only odd numbers
        if test_num % i == 0:
            return False
    return True


def generate_prime_num_list(min_range: int, max_range: int) -> [int]:
    prime_numbers = [i for i in range(min_range, max_range) if is_prime(i)]
    return prime_numbers


# choose two prime numbers
def choose_two_prime_numbers(prime_list: [int]) -> (int, int):
    random.shuffle(prime_list)
    first_prime = prime_list.pop()
    second_prime = prime_list.pop()
    return first_prime, second_prime


# https://www.geeksforgeeks.org/rsa-algorithm-cryptography/
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def get_e(phi_n_value: int) -> int:
    # choose random number from 10 to phi_n_value//128
    rand_e_iter_min = random.randrange(10, phi_n_value//128)
    for e_iter in range(rand_e_iter_min, phi_n_value):
        if gcd(e_iter, phi_n_value) == 1:
            return e_iter


# generate prime list to choose from
prime_num_list = generate_prime_num_list(50, 100)
# random choose p and q
p, q = choose_two_prime_numbers(prime_num_list)
# p, q = 19, 71
# determine n (public key)
n = p*q
# determine phi(n)
phi_n = (p-1)*(q-1)
# choose e (public key)
e = get_e(phi_n)
# compute unique number d (private key)

print(f'p: {p}\nq: {q}\nn: {n}\nphi_n: {phi_n}\ne: {e}')



# # letter codes
# letter_codes = {10: 'A', 55: 'N',
#                 20: 'B', 65: 'O',
#                 30: 'C', 75: 'P',
#                 40: 'D', 85: 'Q',
#                 50: 'E', 95: 'R',
#                 60: 'F', 12: 'S',
#                 70: 'G', 22: 'T',
#                 80: 'H', 32: 'U',
#                 90: 'I', 42: 'V',
#                 15: 'J', 52: 'W',
#                 25: 'K', 62: 'X',
#                 35: 'L', 72: 'Y',
#                 45: 'M', 82: 'Z',
#                 44: ' '}
#
# # e, n, and my d values
# my_e = 47
# my_n = 1349
# my_d = 563
#
# amanda_e = 11
# amanda_n = 869
#
# print("\nmy_e = 47\nmy_n = 1349\nmy_d = 563\n\namanda_e = 313\namanda_n = 1271\n")
#
# # my word: "magic sword"
# word = [45, 10, 70, 90, 30, 44, 12, 52, 65, 95, 40]
#
# actual_word = ""
# # decode my word using 'letter_codes'
# for letter_code in word:
#     actual_word += letter_codes[letter_code]
# # print my word decoded - "magic sword"
# print("My message: " + actual_word)
#
# # ------------------------ Encrypt --------------------------------
# my_encrypted_word = []
# for letter in word:
#     letter_To_MyD = letter**my_d  # (coded letter)^(my_d)
#
#     letter_To_MyD_Mod_MyN = letter_To_MyD % my_n  # [(coded letter)^(my_d)] mod (my_n)
#
#     letter_To_MyD_Mod_MyN_ToAman_E = letter_To_MyD_Mod_MyN**amanda_e
#
#     letter_To_MyD_Mod_MyN_ToAman_E_mod_AmanN = letter_To_MyD_Mod_MyN_ToAman_E % amanda_n
#
#     my_encrypted_word.append(letter_To_MyD_Mod_MyN_ToAman_E_mod_AmanN)
#
# print("My encrypted message: [" + ', '.join(str(e) for e in my_encrypted_word) + "]")
#
# # -------------------------- Decrypt --------------------------------
#
# amanda_encrypted_word = [596, 731, 77, 779, 791, 1168, 913, 1015]
# # print amanda's encrypted word
# print("\nAndy's encrypted message: [" + ', '.join(str(e) for e in amanda_encrypted_word) + "]")
#
# amanda_decrypted_word = []
#
# for encrypted_letter in amanda_encrypted_word:
#     # raise to my_d mod my_n
#     intermediate_value = (encrypted_letter**my_d) % my_n
#
#     # intermediate value raised to amanda_e mod amanda_n
#     decrypted_letter = (intermediate_value**amanda_e) % amanda_n
#
#     # add decrypted letter to decrypted word list
#     amanda_decrypted_word.append(decrypted_letter)
#
# print("Andy's decrypted message: [" + ', '.join(str(e) for e in amanda_decrypted_word) + "]")
#
# # decode Amanda's decrypted message
# actual_amanda_word = ""
# for amanda_letter_code in amanda_decrypted_word:
#     actual_amanda_word += letter_codes[amanda_letter_code]
#
# # print Amanda's decoded word
# print("Andy's decoded message: " + actual_amanda_word)