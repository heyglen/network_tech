# network_tech

Cisco syntax highlighting and completions for Sublime Text 3.

## Documentation

### Syntax and Snippets

![Cisco IOS Demo](/docs/img/cisco_ios_demo.gif)

Notice that the syntax and completions are [aware of the configuration mode](docs/configuration_modes.md). You must exit out configuration modes using the `exit` command as if you were using the actual command line.

### Mask Conversions

![Mask Conversions Demo](/docs/img/mask_conversions_demo.gif)

There are completions that convert between the different IPv4 mask types:
 * Prefix Length
 * Subnet Mask
 * Wildard Mask

The conversions are activated by typing the mask or opening the completions menu (Win: Ctrl+Space).

### Supported Syntax & Completions
 * Cisco ACE
 * Cisco IOS
 * Cisco NXOS
 * Cisco ASA

## Installation

Install using Sublime Text 3 [Package Manager](https://sublime.wbond.net/installation).

*Sublime Text 2 is not supported*

## Feature Requests and Bug Reporting

The goal is to have highlighting and completions on frequently used commands, not full coverage.

[network_tech GitHub Issues](https://github.com/heyglen/network_tech/issues)
