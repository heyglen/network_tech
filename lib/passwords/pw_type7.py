# Copyright 2017 Glen Harmon

import re
import itertools

ios_password_re = re.compile(r'^(?P<salt_index>[01]\d)(?P<encrypted_text>\S{1,25})', re.I)


TRANSLATION_KEY_MAP = 'dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87'


def decode(password):
    if ios_password_re.match(password):
        return ios_decode(password)
    else:
        return nxos_decode(password)


def nxos_decode(password):
    """ See https://networkengineering.stackexchange.com/questions/27987/tacacs-implentation-server-key-error """
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase = uppercase.lower()
    decoded_password = list()
    cipher = [3, 22, 4, 5, 18, 0, 21, 5, 18, 3, 10, 5, 16, 22, 4, 16, 24, 17, 12, 5, 21, 18, 5, 22, 19, 7]
    for character, key in zip(password, itertools.cycle(cipher)):
        if character in lowercase:
            decoded = ord(character) - 97 - key
            if decoded < 0:
                decoded += 26
            decoded += 97
            decoded_password.append(chr(decoded))
        elif character in uppercase:
            decoded = ord(character) - 65 - key
            if decoded < 0:
                decoded += 26
            decoded += 65
            decoded_password.append(chr(decoded))
        else:
            decoded_password.append(character)
    return ''.join(decoded_password)


def ios_decode(password):
    """ Following https://pen-testing.sans.org/resources/papers/gcih/cisco-ios-type-7-password-vulnerability-100566 """
    decoded_password = ''

    # Example Password:
    #   Encoded: 044B0A151C36435C0D
    #   Decoded: password

    # "044B0A151C36435C0D" -> "04" -> 4
    translation_key_index = int(password[0:2])

    # Example is decoding the 'p' from 'password'
    for password_index in range(2,len(password),2):

        # Step 1
        # Get the encoded value

        # Encoded '044B0A151C36435C0D' -> '4B'
        encoded_value = password[password_index:password_index + 2]
        
        # Hex to integer '4B' -> 75
        encoded_value = int(encoded_value, 16)

        # Step 2
        # Get the translation key

        # 'dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87'[4] -> ';'
        translation_key = TRANSLATION_KEY_MAP[translation_key_index]

        # Unicode code point of the tranlation key character
        # ';' -> 59
        translation_key = ord(translation_key)

        # Step 3
        # Preform the decode

        # XOR (^) 75 ^ 59 -> 112
        decoded_value = encoded_value ^ translation_key

        # decoded_password += chr(int(password[password_index] \
        #     + password[password_index+1], 16) \
        #     ^ ord(TRANSLATION_KEY[salt]))
        # salt += 1

        # char(112) -> 'p'
        decoded_password += chr(decoded_value)

        # Step 4:
        # Setup for the next round of decoding
        
        translation_key_index += 1

        if translation_key_index == 53:
            translation_key_index = 0

    return decoded_password