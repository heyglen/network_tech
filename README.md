# sublime-network


Network configuration syntax, completions and snippets for Sublime Text

**Installation**

Download and intstall git

Sublime Text -> Preferences -> Browse Packages...
 
Browse to the User folder

Open Git Bash (Windows: Right click in folder -> Git Bash)

In the bash console type:
```Shell
git clone https://github.com/heyglen/sublime-network.git
```
**Update**

Sublime Text -> Preferences -> Browse Packages...
 
Browse to the User folder

Open Git Bash (Windows: Right click in folder -> Git Bash)

In the bash console type:
```Shell
git pull
```

**Feature Requests and Bug Reporting**

[Sublime-Network GitHub Issues](https://github.com/heyglen/sublime-network/issues)

**Use**

Open the command prompt (Windows: Ctrl+Shift+p) and type one of the following:
 * Set Syntax: Cisco ACE
 * Set Syntax: Cisco IOS
 * Set Syntax: Cisco ASA

**Useful Settings**

To be prompted with the snippets and auto-completions:

Sublime Text -> Preferences -> Settings - User

Add the sublime-network scope to auto completions setting:
```JSON
{
"auto_complete_selector": "source - comment, meta.tag - punctuation.definition.tag.begin, text.network",
...
}
```
