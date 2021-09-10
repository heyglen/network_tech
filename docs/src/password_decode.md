# Password Decode

Some password types can be decoded locally on your computer.

!!! important
    
    The code is linked to below so you can verify it does nothing nefarious.

To decode use the command:

1. In the command pallet choose: `Network Tech: Decode Passwords`

2. Choose the password from the list

3. Choose to display the password in a dialog or copy it to the clipboard

Details on the supported password types and how they are decoded are listed below.

## Type 5

Type 5 passwords are salted MD5 hashes. They can be created using the `openssl` command:

```bash
openssl passwd -1 -salt SpMm password
```

Decoding is done using brute force with an included dictionary of the 10k most common passwords. This means that not all passwords can be broken and the speed of the command increases with out uncommon the password is.

The password dictionary source is [SecLists 10k Most Common](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10k-most-common.txt)

Check the decode implementation used in this plugin [here](https://github.com/heyglen/network_tech/tree/master/lib/passwords/pw_type5.py)

## Type 7

Type 7 passwords are a Cisco proprietary encryption algorithm.

Decoding is done using the [well documented algorithm](https://pen-testing.sans.org/resources/papers/gcih/cisco-ios-type-7-password-vulnerability-100566)

Check the decode implementation used in this plugin [here](https://github.com/heyglen/network_tech/tree/master/lib/passwords/pw_type7.py)
