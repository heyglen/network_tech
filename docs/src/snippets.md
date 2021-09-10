# Completions

Configuration snippets and auto completions are suggested based off the syntax and configuration mode.

!!! hint

    Completions are selected by fuzzy matching what you type.

    "**shipintbr**" will match "**show ip interface brief**".

    "**show ip**" will match completions starting with "**ip**"–*not* "**show ip**".

    Avoid typing spaces to match more specific completions.

## Mask Conversions

Manually Trigger the Completions Popup: :keyboard:`<ctrl>+<space>`

![](/img/mask_conversions_demo.gif)

There are mask completions that convert between the different IPv4 mask types:

* Prefix Length: /24

* Subnet Mask: 255.255.255.0

* Wildcard Mask: 0.0.0.255

The conversions are activated by typing the mask or opening the completions menu:

- :fontawesome-brands-windows: :keyboard: `ctrl+space`
