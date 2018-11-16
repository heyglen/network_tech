
import re

password_re = re.compile(r'^(?P<salt_index>[01]\d)(?P<encrypted_text>[0-9a-f]{1,25})', re.I)


TRANSLATION_KEY = 'tfd;kfoA,.iyewrkldJKD'

# Following https://pen-testing.sans.org/resources/papers/gcih/cisco-ios-type-7-password-vulnerability-100566

def decode(password):
    decoded_password = ''
    if not password_re.match(password):
        return 'Invalid Type 7 Password'
    # Step 1
    # Take the first two digits of the encrypted text.
    salt_index = int(password[0:2]) - 1

    for password_index in range(2, len(password), 2):
        # Step 2
        # Obtain the current salt.
        salt = ord(TRANSLATION_KEY[salt_index])
        salt_index += 1

        # Step 3
        # Take the next two digits of the encrypted text        
        encrypted_text_index = password_index
        encrypted_text_index_end = encrypted_text_index + 2

        encrypted_characters = password[encrypted_text_index:encrypted_text_index_end]
        encrypted = int(encrypted_characters, 16)

        # Step 4
        # Calculate the first plaintext character in the password.            
        decrypted = encrypted ^ salt
        character = chr(decrypted)

        decoded_password += character

    return decoded_password

