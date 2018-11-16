Password Decode
===============

.. Important::
    
    All password decoding is done locally on your machine

    Verify in the code:
        
    `Type 5 Decode <https://github.com/heyglen/network_tech/tree/master/lib/pw_type5>`_    

    `Type 7 Decode <https://github.com/heyglen/network_tech/tree/master/lib/pw_type7>`_    


Type 5
------

Password decode method: Brute Force - 10k most common passwords 

If the password can be brute forced, then mousing over the command

``enable secret 5 $1$SpMm$eALjeyED.WSZs0naLNv21/``

will display a popup with the clear text password

Password source: `SecLists 10k Most Common <https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10k-most-common.txt>`_

Type 7
------

Mouse over type 7 passwords such as ``enable password 7 0822455D0A16``` to get the clear text password
