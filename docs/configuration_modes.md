## Configuration Modes

The syntax and snippets are aware of the current configuration mode of your configuration. 

The side effect of this is that in order for them to work, you must explicitly enter and exit configuration modes.

You exit out of configuration modes using `exit` just as you would in the cli.

The default configuration mode is *enable*.

### Example

**Incorrect**
   ```
   hostname router01
   ```

Since you can only set the hostname in `configure terminal` mode. 

**Correct**
   ```
   configure terminal
     hostname router01
   exit
   ```

You must exit out of all configuration modes:

**Incorrect**
   ```
   configure terminal
     interface eth1
       description blah blah blah
    hostname switch01
   exit
   ```
In this example the interface configuration mode was never exited out of so the configuration mode command `hostname switch01` is not valid

**Correct**
   ```
   configure terminal
     interface Ethernet1
       description blah blah blah
      exit
     hostname switch01
   exit
   ```
