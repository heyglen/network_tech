# sublime-network


Network configuration syntax highlighting, completions and snippets for Sublime Text.

Supports:
 * Cisco ACE
 * Cisco IOS
 * Cisco NXOS
 * Cisco ASA

## Usage

Open the command prompt (Windows: Ctrl+Shift+p) and type one of the following:
 * Set Syntax: Cisco ACE
 * Set Syntax: Cisco IOS
 * Set Syntax: Cisco NXOS
 * Set Syntax: Cisco ASA

### Configure Auto Completion Suggestion Settings

To be prompted with the snippets and auto-completions:

Sublime Text -> Preferences -> Settings - User

Add the sublime-network scope to auto completions setting in between the brackets:
```JSON
{
"auto_complete_selector": "text.network",
}
```
## Installation

[Install Sublime Text 3](http://www.sublimetext.com/3)

[Install Sublime Package Manager](https://sublime.wbond.net/installation)

Sublime Text -> Tools -> Command Pallet

Type add repository

In the text box that appears docked to the bottom type:

https://github.com/heyglen/sublime-network

## Feature Requests and Bug Reporting

[Sublime-Network GitHub Issues](https://github.com/heyglen/sublime-network/issues)
