# Completions

Configuration snippets and auto completions are suggested based off the syntax and configuration mode.

!!! hint

    There are *many* command completions. Many commands start the same:

    * {++show ip++} interface brief

    * {++show ip++} route

    Avoid typing spaces to better match the completion you are after.

    Completions are selected by fuzzy matching what you type.

    "**shipintbr**" will match "**show ip interface brief**".

    "**show ip**" will match completions starting with "**ip**"–*not* "**show ip**".

## Mask Conversions

![](/img/mask_conversions_demo.gif)

!!! warning

    This will only work with one of the Network Syntax set (Cisco IOS, Cisco NXOS, etc)


There are mask completions that convert between the different IPv4 mask types:

* Prefix Length: /24

* Subnet Mask: 255.255.255.0

* Wildcard Mask: 0.0.0.255

The conversions are suggested as completions when typing the mask, prefix or wildcard.
