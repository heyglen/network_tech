# sublime-network


Network configuration syntax highlighting, completions and snippets for Sublime Text.

Supports:
 * Cisco ACE
 * Cisco IOS
 * Cisco NXOS
 * Cisco ASA

**Usage**

Open the command prompt (Windows: Ctrl+Shift+p) and type one of the following:
 * Set Syntax: Cisco ACE
 * Set Syntax: Cisco IOS
 * Set Syntax: Cisco NXOS
 * Set Syntax: Cisco ASA

**Configure Auto Completion Suggestion Settings**

To be prompted with the snippets and auto-completions:

Sublime Text -> Preferences -> Settings - User

Add the sublime-network scope to auto completions setting in between the brackets:
```JSON
{
"auto_complete_selector": "text.network",
...
}
```
**Installation**

Download and intstall git

Sublime Text -> Preferences -> Browse Packages...
 
Browse to the User folder

Open Git Bash (Windows: Right click in folder -> Git Bash)

In the bash console type:
```Shell
git clone https://github.com/heyglen/sublime-network.git
```

**Updates**

Sublime Text -> Preferences -> Browse Packages...
 
Browse to the User folder

Open Git Bash (Windows: Right click in folder -> Git Bash)

In the bash console type:
```Shell
git pull
```

**Feature Requests and Bug Reporting**

[Sublime-Network GitHub Issues](https://github.com/heyglen/sublime-network/issues)
