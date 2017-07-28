import sys
import re
import ipaddress
import contextlib
import logging

import sublime
import sublime_plugin

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
logger.handlers = []
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(*args):
        val = dict.get(*args)
        return DotDict(val) if type(val) is dict else val


ip = DotDict({
    'v4': {
        'host': re.compile(r'(?:\d{1,3}\.){3}\d{1,3}'),
        'any': re.compile(
            r"""
            (?xi)
            (?:
                \b
                (?P<ip>(?:\d{1,3}\.){3}\d{1,3})
                (?:
                    (?:/(?P<prefix_length>\d{2}\b))|
                    (?:
                        \s+
                        (?:
                            (?:mask\s+)?
                            (?P<netmask>(\d{1,3}\.){3}\d{1,3})
                        )
                    )
                )?
            )
            """
        ),
        'network': {
            'netmask': re.compile(r'(?:(?:\d{1,3}\.){3}\d{1,3} (?:\d{1,3}\.){3}\d{1,3})'),
        }
    }
})

sublime_ip = DotDict({
    'v4': {
        'any': re.compile(
            r"""(?:\b(?:(?:\d{1,3}\.){3}\d{1,3})(?:(?:/(?:\d{2}\b))|(?:\s+(?:(?:mask\s+)?(?:(\d{1,3}\.){3}\d{1,3}))))?)"""

        ),
        'host': re.compile(r'(?:(?:\d{1,3}\.){3}\d{1,3})'),
        'network': {
            'netmask': re.compile(r'(?:(?:\d{1,3}\.){3}\d{1,3} (?:\d{1,3}\.){3}\d{1,3})'),
            'cidr': re.compile(r'\d?\d?\d\.\d?\d?\d\.\d?\d?\d\.\d?\d?\d/\d?\d'),
        }
    }
})


class FindSubnetCommand(sublime_plugin.TextCommand):
    def network_contains(self, member, group):
        result = False
        if isinstance(member, ipaddress.IPv4Address):
            result = member in group
        elif isinstance(member, ipaddress.IPv4Network):
            result = int(group.network_address) <= int(member.network_address) and \
                int(group.broadcast_address) >= int(member.broadcast_address)
        return result

    def coerce_network(self, network):
        network = network.strip()
        try:
            network_object = ipaddress.ip_address(network)
        except ValueError:
            network_parts = network.split()
            cleaned_network = network
            if len(network_parts) is 2:
                cleaned_network = '/'.join(network_parts)    
            try:
                network_object = ipaddress.ip_interface(cleaned_network).network
            except ValueError:
                network_object = None
        return network_object

    def get_network(self, network, find_all=False):
        search_network = self.coerce_network(network)
        logger.debug('Searching for network {}'.format(search_network))
        if search_network is None:
            logger.debug('Invalid network {}'.format(network))
        else:
            for region in self.view.sel():
                logger.debug('Start search at point {}'.format(region.begin()))
                logger.debug('Searching for {}'.format(sublime_ip.v4.any.pattern))

                found_region = self.view.find(
                    sublime_ip.v4.any.pattern,
                    region.end(),
                    sublime.IGNORECASE
                )
                if found_region:
                    found_network = self.coerce_network(self.view.substr(found_region))
                    if not self.network_contains(found_network, search_network):
                        continue

                    self.view.show_at_center(found_region.begin())
                    self.view.sel().clear()
                    logger.debug('Found region {} {}'.format(found_region.begin(), found_region.end()))
                    self.view.sel().add(sublime.Region(
                        found_region.begin(),
                        found_region.end()
                    ))
                else:
                    logger.debug('{} not found'.format(search_network))
        self._find_input_panel(network)

    def _find_input_panel(self, network=''):
        self.view.window().show_input_panel(
            caption='Find a network',
            initial_text=network,
            on_done=self.get_network,
            on_change=None,
            on_cancel=None
        )

    def run(self, edit):
        self._find_input_panel()

class SubnetCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            text = self.view.substr(region)
            self.view.replace(edit, region, text + 'hi')
