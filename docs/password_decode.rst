Password Decode
===============

The password types below can be locally decoded using various methods.

.. Important::
    
    The code is linked to below so you can verify it does nothing nefarious.

To decode use the command `Network Tech: Brute Force Type [type number] Passwords` in the command pallet

Type 5
------

Type 5 passwords are salted MD5 hashes. They can be created using the openssl command:

.. code-block:: shell

    openssl passwd -1 -salt SpMm password

Decoding is done using brute force limited to an included dictionary of the 10k most common passwords.

The password dictionary source is `SecLists 10k Most Common <https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10k-most-common.txt>`_

Check the decode implementation used in this plugin `here <https://github.com/heyglen/network_tech/tree/master/lib/passwords/pw_type5.py>`_

Type 7
------

Type 7 passwords are a Cisco propriatary encryption algorithm.

Decoding is done using the `well documented algorithm <https://pen-testing.sans.org/resources/papers/gcih/cisco-ios-type-7-password-vulnerability-100566>`_.

Check the decode implementation used in this plugin `here <https://github.com/heyglen/network_tech/tree/master/lib/passwords/pw_type7.py>`_
