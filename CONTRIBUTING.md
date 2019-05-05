# Contributing

When contributing to this repository, please first discuss the change you wish to make via an issue with the owners of the repository before making a change.

Changes should be submitted using the pull request process.

## Change Log

Changes, features, and bug fixes are documented in a changelog files located in messages/<version>.md

New changelogs should be referenced in the messages.json file

Changelogs follow the [Keep a Changelog Standard](http://keepachangelog.com)

## Testing

### Syntax

- New syntax should be written in the relevant test files:
    - [ios: tests/syntax_test_cisco_ios.cisco-ios](tests/syntax_test_cisco_ios.cisco-ios)
    - [ios-xr: tests/syntax_test_cisco_ios_xr.cisco-ios-xr](tests/syntax_test_cisco_ios_xr.cisco-ios-xr)
    - [nxos: tests/syntax_test_cisco_nxos.cisco-nxos](tests/syntax_test_cisco_nxos.cisco-nxos)
    - [asa: tests/syntax_test_cisco_asa.cisco-asa](tests/syntax_test_cisco_asa.cisco-asa)
    - [ace: tests/syntax_test_cisco_ace.cisco-ace](tests/syntax_test_cisco_ace.cisco-ace)
- These files are used for testing the syntax by visual inspection
