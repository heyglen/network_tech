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
                (?:
                    (?:
                        (?:host)|
                        (?:range)
                    )\s+(?:(?:\d{1,3}\.){3}\d{1,3})
                )|
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

class SearchHistory(list):
    @property
    def last(self):
        last = None
        if self:
            last = self[0]
        return last

search_history = SearchHistory()


class Network:
    prefix_removals = [
        'host',
        'mask',
        'range'
    ]

    @classmethod
    def contains(self, group, member):
        return int(group.network_address) <= int(member.network_address) and \
            int(group.broadcast_address) >= int(member.broadcast_address)

    @classmethod
    def clean(cls, network_text):
        for remove in cls.prefix_removals:
            network_text = network_text.replace(remove, '')
        network_text = network_text.strip()
        return network_text

    @classmethod
    def get(cls, network_text):
        network_text = cls.clean(network_text)
        try:
            network = ipaddress.ip_address(network_text)
            network = ipaddress.ip_network(network_text + '/32')
        except ValueError:
            network_parts = network_text.split()
            cleaned_network = network_text
            if len(network_parts) is 2:
                cleaned_network = '/'.join(network_parts)
            try:
                network = ipaddress.ip_interface(cleaned_network).network
            except ValueError:
                network = None
        return network

    @classmethod
    def clean_region(cls, view, region):
        text = view.substr(region)
        for remove in cls.prefix_removals:
            if text.startswith(remove):
                cleaned = text.replace(remove, '').strip()
                removed_characters = len(text) - len(cleaned)
                return sublime.Region(region.begin() + removed_characters, region.end())
        return region

    @classmethod
    def clean_regions(cls, view, regions):
        cleaned = list()
        for region in regions:
            cleaned = cls.clean_region(view, region)
        return cleaned

class FindSubnetCommand(sublime_plugin.TextCommand):

    def get_network(self, network, find_all=False):
        search_history.append(network)
        search_network = Network.get(network)

        current_regions = self.view.sel()

        logger.debug('Searching for network {}'.format(search_network))
        if not search_network:
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
                    found_network = Network.get(network_re_match)

                    if Network.contains(search_network, found_network):
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
        default_search = '10.139.4.0/24' if not search_history else search_history.last
        self._find_input_panel(network=default_search)


class FindAllSubnetsCommand(sublime_plugin.TextCommand):

    def get_network(self, networks, find_all=False):
        search_history.append(networks)

        search_networks = {Network.get(n) for n in networks.split(',')}

        current_regions = self.view.sel()

        logger.debug('Searching for network(s) {}'.format(networks))
        for network in search_networks:
            if not network:
                message = 'Invalid network {}'.format(network)
                logger.debug(message)
                self.view.show_popup_menu(message)
                return
        else:
            user_regions = self.view.sel()
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(0, 0))

            found_regions = self.view.find_all(
                sublime_ip.v4.any,
                sublime.IGNORECASE,
            )

            matching_networks = set()
            found_networks = {self.view.substr(r) for r in found_regions}
            logger.debug('Found {} IP like objects'.format(len(found_networks)))
            for found_network in found_networks:
                if found_network in matching_networks:
                    continue
                logger.debug('Getting network "{}"'.format(found_network))
                
                for search_network in search_networks:
                    network_object = Network.get(found_network)
                    if network_object and Network.contains(search_network, network_object):
                        matching_networks.add(found_network)
                        break

            self.view.sel().clear()
            if matching_networks:
                moved_view = False
                for region in found_regions:
                    cleaned_region = Network.clean_region(self.view, region)
                    if self.view.substr(cleaned_region) in matching_networks:
                        self.view.sel().add(cleaned_region)
                        if not moved_view:
                            self.view.show_at_center(cleaned_region.begin())
                            moved_view = True
            else:
                logger.debug('No matches')
                self.view.sel().add_all(current_regions)
                self.view.show_at_center(current_regions[0].begin())

        # self._find_input_panel(networks)

    def _find_input_panel(self, network=''):
        self.view.window().show_input_panel(
            caption='Find all Network(s) - comma seperated',
            initial_text=network,
            on_done=self.get_network,
            on_change=None,
            on_cancel=None
        )

    def run(self, edit):
        default_search = '10.139.4.0/24' if not search_history else search_history.last
        self._find_input_panel(network=default_search)

