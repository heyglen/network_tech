# Copyright 2017 Glen Harmon

import re

password_re = re.compile(r'^(?P<salt_index>[01]\d)(?P<encrypted_text>[0-9a-f]{1,25})', re.I)


TRANSLATION_KEY='dsfd;kfoA,.iyewrkldJKDHSUBsgvca69834ncxv9873254k;fg87'

# Following https://pen-testing.sans.org/resources/papers/gcih/cisco-ios-type-7-password-vulnerability-100566

def decode(password):
    decoded_password = ''
    if not password_re.match(password):
        return 'Invalid Type 7 Password'
    salt= int(password[0:2])
    for password_index in range(2,len(password),2):
        decoded_password += chr(int(password[password_index] \
            + password[password_index+1], 16) \
            ^ ord(TRANSLATION_KEY[salt]))
        salt += 1
        if salt==53:salt=0

    return decoded_password
