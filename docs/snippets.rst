Completions 
======

Configuration snippets and autocompetions are suggested based off the syntax and configuration mode.

Mask Conversions
----------------

Manually Trigger the Completions Popup: ⌨ :kbd:`<ctrl>+<space>`

.. image:: /_images/mask_conversions_demo.gif

There are mask completions that convert between the different IPv4 mask types:
 * Prefix Length: /24
 * Subnet Mask: 255.255.255.0
 * Wildard Mask: 0.0.0.255

.. note::

    Prefix lengths will only complete if there is a space before the '/' character
    
    - Right: " /24 "
    - Wrong: " 1.2.3.4/24 "


The conversions are activated by typing the mask or opening the completions menu:

 - Windows: :kbd:`ctrl-space`
