# Copyright 2017 Glen Harmon

import functools
import importlib
import ipaddress
import logging
import re

import sublime
import sublime_plugin

logger = logging.getLogger("network_tech.increment.network.network")

Network = importlib.import_module("Network Tech.lib.search.network.network").Network

WILDCARD_RE = re.compile(
    r"""
    (?xi)
    (?:
        (?:127\.255\.255\.255)|
        (?:63\.255\.255\.255)|
        (?:31\.255\.255\.255)|
        (?:15\.255\.255\.255)|
        (?:7\.255\.255\.255)|
        (?:3\.255\.255\.255)|
        (?:1\.255\.255\.255)|
        (?:0\.255\.255\.255)|
        (?:0\.127\.255\.255)|
        (?:0\.63\.255\.255)|
        (?:0\.31\.255\.255)|
        (?:0\.15\.255\.255)|
        (?:0\.7\.255\.255)|
        (?:0\.3\.255\.255)|
        (?:0\.1\.255\.255)|
        (?:0\.0\.255\.255)|
        (?:0\.0\.127\.255)|
        (?:0\.0\.63\.255)|
        (?:0\.0\.31\.255)|
        (?:0\.0\.15\.255)|
        (?:0\.0\.7\.255)|
        (?:0\.0\.3\.255)|
        (?:0\.0\.1\.255)|
        (?:0\.0\.0\.255)|
        (?:0\.0\.0\.127)|
        (?:0\.0\.0\.63)|
        (?:0\.0\.0\.31)|
        (?:0\.0\.0\.15)|
        (?:0\.0\.0\.7)|
        (?:0\.0\.0\.3)|
        (?:0\.0\.0\.1)
    )
"""
)


class IncrementSubnetCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        increment_prefix_length(view=self.view, edit=edit, amount=1)


class DecrementSubnetCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        increment_prefix_length(view=self.view, edit=edit, amount=-1)


class IncrementNetworkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        increment_network(view=self.view, edit=edit, amount=1)


class DecrementNetworkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        increment_network(view=self.view, edit=edit, amount=-1)


class IncrementIpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        increment_ip(view=self.view, edit=edit, amount=1)


class DecrementIpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        increment_ip(view=self.view, edit=edit, amount=-1)


def _get_ip_object(value, view, region):
    if _is_wildcard(ip=value, view=view, region=region):
        ip, wildcard = value.split()
        # Thanks
        # https://medium.com/opsops/wildcard-masks-operations-in-python-16acf1c35683
        wildcard_ip = ipaddress.IPv4Address(wildcard)
        netmask = str(ipaddress.IPv4Address(int(wildcard_ip) ^ (2 ** 32 - 1)))
        value = "{} {}".format(ip, netmask)
    result = None
    try:
        result = ipaddress.ip_interface(value.replace(" ", "/"))
    except ValueError:
        pass
    return result


def _is_wildcard(ip, view, region):
    try:
        _, wildcard_mask = ip.split()
    except ValueError:
        return False
    index = ip.rindex(wildcard_mask)
    point = region.begin() + index
    scope = view.scope_name(point).split()
    if "constant.numeric.network.ipv4.wildcard" in scope:
        return True
    is_wildcard = bool(WILDCARD_RE.match(wildcard_mask))
    return is_wildcard


def _format_ip(original, ip, view, region):
    text = str(ip)

    if "/" not in original and " " not in original:
        text = str(ip.ip)
    elif ip.version == 4:
        if " " in original:
            if _is_wildcard(ip=original, view=view, region=region):
                text = ip.with_hostmask.replace("/", " ")
            else:
                text = "{} {}".format(ip.ip, ip.netmask)
    return text


def increment(invert_on_wildcard=False):
    def increment_inner(fn):
        def wrapper(view, edit, amount=1):
            modified_regions = list()
            for cursor_region in view.sel():
                region = Network.get_network_region(cursor_region, view)
                if region is None:
                    modified_regions.append(cursor_region)
                    continue
                original_network_string = view.substr(region)
                ip_interface = _get_ip_object(
                    value=original_network_string, view=view, region=region
                )

                modified_amount = amount
                if invert_on_wildcard and _is_wildcard(
                    ip=original_network_string, view=view, region=region
                ):
                    modified_amount = amount * -1
                next_address = fn(ip_interface=ip_interface, amount=modified_amount)

                text_address = _format_ip(
                    original=original_network_string,
                    ip=next_address,
                    view=view,
                    region=region,
                )

                view.replace(edit, region, text_address)

                region_end = region.begin() + len(text_address)
                if cursor_region.empty():
                    region_end = region.begin()
                modified_regions.append(sublime.Region(region.begin(), region_end))
            view.sel().clear()
            view.sel().add_all(modified_regions)

        return functools.update_wrapper(wrapper, fn)

    return increment_inner


@increment(invert_on_wildcard=True)
def increment_prefix_length(ip_interface, amount=1):
    is_network = ip_interface.ip == ip_interface.network.network_address
    network = ip_interface.network

    new_prefixlen = network.prefixlen + amount
    if new_prefixlen > network.max_prefixlen:
        new_prefixlen = ip_interface.max_prefixlen
    elif new_prefixlen < 0:
        new_prefixlen = 0

    next_address = ipaddress.ip_interface(
        "{}/{}".format(ip_interface.ip, new_prefixlen)
    )
    if is_network:
        # The input IP was a network address, set the new ip to the network address
        network_address = next_address.network.network_address
        next_address = ipaddress.ip_interface(
            "{}/{}".format(network_address, new_prefixlen)
        )
    return next_address


@increment()
def increment_network(ip_interface, amount=1):
    network = ip_interface.network
    adjust = network.num_addresses * amount
    next_network_ip = ip_interface.ip + adjust
    next_address = ipaddress.ip_interface(
        "{}/{}".format(next_network_ip, network.prefixlen)
    )
    return next_address


@increment()
def increment_ip(ip_interface, amount=1):
    network = ip_interface.network
    ip_interface = ip_interface + amount
    next_address = ipaddress.ip_interface(
        "{}/{}".format(ip_interface.ip, network.prefixlen)
    )
    return next_address
