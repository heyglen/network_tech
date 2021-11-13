# Contributing

When contributing, please first discuss the change you wish to make via an issue with the owners of the repository before making a change.

Changes should be submitted using the pull request process.

## Change Log

Changes, features, and bug fixes must be documented in the changelog file in [`messages/head.md`](https://github.com/heyglen/network_tech/blob/master/messages/head.md)

When a new version is released, this is what is shown to the user.

If the change came about from an issue, link to it. Give credit 🙂

## Quality Standards

!!! note

    These have evolved over time with experience, so unfortunately not everything you see will follow these standards.

    All new features I create follow this.

The purpose of syntax highlighting is to give the user visual feedback of correctness.

The following is a checklist of things to consider when adding new syntax.

* Build syntax after the official documentation (For Cisco commands, this would be the Command Reference)

* Support the entire command in all it's variations, options, etc.

!!! question

    Why?

    Troubleshooting RegEx is hard and fixing other peoples RegEx is even harder. Fully support each command so we can avoid going back to add or fix it later.

!!! example

    For Cisco IOS `show running-config` command should support:

    * `show running-config`

    * `show running-config all`

    * `show run` (a commonly used short hand)

    * `show run all`

    * etc...

* Place the command and all it's variations in the test file

* Link to the command reference you used in the test file over the test commands as a comment

!!! example

    From the [Cisco IOS](https://github.com/heyglen/network_tech/blob/master/tests/syntax_test_cisco_ios.cisco-ios) Syntax:

    ```
    ! https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/security/a1/sec-a1-cr-book/sec-cr-a1.html#wp3188257209
    aaa authentication dot1x default enable
    aaa authentication dot1x default group radius
    aaa authentication dot1x default line
    aaa authentication dot1x default local
    aaa authentication dot1x default local-case
    aaa authentication dot1x default none
    ```


* Create completions for all variations of the command (within reason)

* Respect config contexts as much as possible.

    * OSPF commands should not highlight under a BGP configuration

    * OSPF completions should not be suggested under a BGP configuration

* If only a certain range of numbers is allowed, ensure the syntax only matches valid numbers

    * This is difficult in RegEx. Re-use logic where possible using [Syntax Variables](https://www.sublimetext.com/docs/syntax.html#variables)

    * Follow a naming standard: `number_range_<START>_<END>` → `number_range_1_15`

    * Test your boundary conditions! For `number_range_1_15` ensure `1` & `15` highlights properly, while `0` & `16` does not.

    * You can copy & paste the examples for typical IPv4 & IPv6 formats in the [Cisco IOS](https://github.com/heyglen/network_tech/blob/master/cisco-ios.sublime-syntax) syntax. See the variables:

        * `subnet_mask`

        * `wildcard_mask`

        * `ip`

        * `ipv4_prefix`

        * `ipv4_prefix_length`

        * `ipv6`

        * `ipv6_prefix`

        * `ipv6_prefix_length`

* Use [standard](https://github.com/heyglen/network_tech/blob/master/standards.txt) scope names where possible. For example, IPv4 wildcard masks should always have the scope `constant.numeric.network.ipv4.wildcard`.

* Support Goto Symbol where possible. See [Cisco IOS](https://github.com/heyglen/network_tech/blob/master/cisco-ios.sublime-syntax) for an example.

    * The commands that change the command context are scoped with `cisco.scope`

    * Theses scopes are referred to in the [Symbol Index](https://github.com/heyglen/network_tech/blob/master/Symbol%20Index.tmPreferences)

!!! note

    This is used to assist the [search](https://network-tech.readthedocs.io/en/latest/src/network_search/), [keyboard subnetting](https://network-tech.readthedocs.io/en/latest/src/keyboard-shortcuts/#host) and [password decoding](https://network-tech.readthedocs.io/en/latest/src/password_decode/) features.

!!! example

    *0.0.0.0* is a valid Subnet and Wildcard mask. If the keyboard shortcut to increment / decrement the prefix length is used, the code needs to know if it should output *0.0.0.1* (Wildcard) or *128.0.0.0* (Subnet). The scope provides this information.

## GIT

* One git commit per syntax item. Typically:

    * The [`messages/head.md`](https://github.com/heyglen/network_tech/blob/master/messages/head.md) changelog

    * The `*.sublime-syntax` regex for the command

    * The testing in the [`tests/`](https://github.com/heyglen/network_tech/tree/master/tests) file

    * The associated `*.sublime-completions`


## Releases

Releases are made by the author.

The [tools/release.py](https://github.com/heyglen/network_tech/blob/master/tools/release.py) script automates the process:

* Dates and versions the changelog [`messages/head.md`](https://github.com/heyglen/network_tech/blob/master/messages/head.md) and inserts it into [`messages.json`](https://github.com/heyglen/network_tech/blob/master/messages.json)

* Commits the version bump

* Tags the commit

* Pushes the commit

* Creates a GitHub release

## Testing

Place all supported syntax in a test file in the [`tests/`](https://github.com/heyglen/network_tech/tree/master/tests) folder:

* [IOS: tests/syntax_test_cisco_ios.cisco-ios](https://github.com/heyglen/network_tech/blob/master/tests/syntax_test_cisco_ios.cisco-ios)

* [IOS-XR: tests/syntax_test_cisco_ios_xr.cisco-ios-xr](https://github.com/heyglen/network_tech/blob/master/tests/syntax_test_cisco_ios_xr.cisco-ios-xr)

* [NXOS: tests/syntax_test_cisco_nxos.cisco-nxos](https://github.com/heyglen/network_tech/blob/master/tests/syntax_test_cisco_nxos.cisco-nxos)

* [ASA: tests/syntax_test_cisco_asa.cisco-asa](https://github.com/heyglen/network_tech/blob/master/tests/syntax_test_cisco_asa.cisco-asa)

* [ACE: tests/syntax_test_cisco_ace.cisco-ace](https://github.com/heyglen/network_tech/blob/master/tests/syntax_test_cisco_ace.cisco-ace)

They should be named `syntax_test_<SYNTAX-NAME>.<SYNTAX-FILE-EXTENSION>`

Testing is done by visual inspection of these files
