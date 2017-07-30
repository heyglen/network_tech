import re
import ipaddress
import logging

import sublime
import sublime_plugin

logger = logging.getLogger('net_tech')
# handler = logging.StreamHandler()
# handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
logger.handlers = []
# logger.addHandler(handler)
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
                (?P<ip>(?:\d{1,3}\.){3}\d{1,3})
                (?:
                    (?:/(?P<prefix_length>\d{2}))|
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
            'netmask': re.compile(r'(?:(?:\d{1,3}\.){3}\d{1,3}\s+(?:\d{1,3}\.){3}\d{1,3})'),
        }
    }
})

sublime_ip = DotDict({
    'v4': {
        'any': r"""
            (?:
                (?:host\s+(?:\d{1,3}\.){3}\d{1,3})|
                (?:
                    (?:(?:\d{1,3}\.){3}\d{1,3})
                    (?:
                        (?:/(?:\d{2}))|
                        (?:
                            \s+
                            (?:
                                (?:mask\s+)?
                                (?:(\d{1,3}\.){3}\d{1,3})
                            )
                        )
                    )?
                )
            )
        """.replace(' ', '').replace('\r', '').replace('\n', ''),
        'host': re.compile(r'(?:(?:\d{1,3}\.){3}\d{1,3})'),
        'network': {
            'netmask': re.compile(r'(?:(?:\d{1,3}\.){3}\d{1,3}\s+(?:\d{1,3}\.){3}\d{1,3})'),
            'cidr': re.compile(r'\d?\d?\d\.\d?\d?\d\.\d?\d?\d\.\d?\d?\d/\d?\d'),
        }
    }
})


class FindSubnetCommand(sublime_plugin.TextCommand):
    def network_contains(self, member, group):
        return int(group.network_address) <= int(member.network_address) and \
            int(group.broadcast_address) >= int(member.broadcast_address)

    def coerce_network(self, network):
        for remove in ['host', 'mask']:
            network = network.replace(remove, '')

        network = network.strip()

        try:
            network_object = ipaddress.ip_address(network)
            network_object = ipaddress.ip_network(network + '/32')
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

        current_regions = self.view.sel()

        logger.debug('Searching for network {}'.format(search_network))
        if search_network is None:
            logger.debug('Invalid network {}'.format(network))
        else:
            for region in self.view.sel():
                cursor = region.end()
                searched_from_start = cursor is 0

                while True:
                    found_region = self.view.find(
                        sublime_ip.v4.any,
                        cursor,
                        sublime.IGNORECASE
                    )

                    if not found_region:
                        self.view.sel().clear()

                        if not searched_from_start:
                            self.view.sel().add(sublime.Region(0, 0))
                            searched_from_start = True
                            cursor = 0
                            continue

                        self.view.sel().add_all(current_regions)
                        break

                    network_re_match = self.view.substr(found_region)
                    logger.debug('Network RE match {}'.format(network_re_match))
                    found_network = self.coerce_network(network_re_match)

                    if found_network.overlaps(search_network):
                        self.view.sel().clear()
                        self.view.show_at_center(found_region.begin())
                        logger.debug('Found region {} {}'.format(found_region.begin(), found_region.end()))
                        self.view.sel().add(sublime.Region(
                            found_region.begin(),
                            found_region.end()
                        ))
                        break
                    cursor = found_region.end()

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
        self._find_input_panel(network='1.1.1.1/24')


class SubnetCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            text = self.view.substr(region)
            self.view.replace(edit, region, text + 'hi')
