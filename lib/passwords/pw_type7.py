# Copyright 2017 Glen Harmon

import re

password_re = re.compile(r'^(?P<salt_index>[01]\d)(?P<encrypted_text>[0-9a-f]{1,25})', re.I)


TRANSLATION_KEY_MAP = 'dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87'

# Following https://pen-testing.sans.org/resources/papers/gcih/cisco-ios-type-7-password-vulnerability-100566

def decode(password):
    decoded_password = ''
    if not password_re.match(password):
        return 'Invalid Type 7 Password'

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