"""
Copyright 2017 Glen Harmon

"""


import os
import pathlib
import ipaddress
import logging
import sys

import sublime

from .html_helper import Html
from .selection_utility import SelectionUtility
from .variables import ip

installed_pacakges = str(pathlib.Path(__file__).parent.parent.parent.parent)
sys.path.append(installed_pacakges)

from network_tech.lib.iana import Iana


logger = logging.getLogger('network_tech.search.network.network')


iana = Iana(os.path.sep.join(['network_tech', 'iana.cache']))



class Network:
    prefix_removals = [
        'host',
        'mask',
        'range'
    ]

    @classmethod
    def info(cls, network):
        """ Returns HTML formated information about the network """
        content = ''
        if network.network.num_addresses is 1:
            content = cls._info_address(network)
        else:
            content = cls._info_network(network)
        return content
        # elif isinstance(network, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
        #     pass
    
    @classmethod
    def _info_address(cls, ip):
        content = Html.div('IP: {}'.format(ip.ip))
        return content

    @classmethod
    def _info_network(cls, network):
        content = ''
        neighbors = cls.get_neighbors(network)
        logger.debug('Neighbors {}'.format(len(neighbors)))
        before, _, after = cls.get_neighbors(network)
        network_address = str(network.network.network_address)
        broadcast_address = str(network.network.broadcast_address)
        if network_address != broadcast_address:
            if network.version is 4:
                content = ''.join([
                    Html.div('Network: {}'.format(network.network)),
                    Html.div('Broadcast: {}'.format(broadcast_address)),
                    Html.div('# Addresses: {}'.format(network.network.num_addresses)),
                    Html.div('Masks:'),
                    Html.unordered_list(Network.masks(network)),
                ])
            else:
                content = ''.join([
                    Html.div('Network: {}/{}'.format(network_address, network.network.prefixlen)),
                ])

            if before or after:
                content += Html.div('Neighboring Networks')
            if after:
                content += Html.div(' Next: {}'.format(after.network))
            if before:
                content += Html.div(' Previous: {}'.format(before.network))
        return content


    @classmethod
    def rir(cls, network):
        rir = iana.get_registrar(network)
        if rir is not None:
            content = Html.div('RIR: {}'.format(rir))
        else:
            content = ''
        return content

    @classmethod
    def _neighboring_network(cls, interface, after=True):
        prefix = interface.network.prefixlen
        network = interface.network
        try:
            neighbor = network.broadcast_address + 1 if after else network.network_address - 1
        except ipaddress.AddressValueError:
            return None
        return ipaddress.ip_interface('{}/{}'.format(neighbor, prefix))

    @classmethod
    def get_neighbors(cls, networks, neighbors=1):
        if not isinstance(networks, list):
            networks = [networks]
        if len(networks) is 0:
            raise ValueError('No network defined')

        before = cls._neighboring_network(networks[0], after=False)
        after = cls._neighboring_network(networks[-1], after=True)

        networks.insert(0, before)
        networks.append(after)

        remaining_neighbors = neighbors - 1
        if remaining_neighbors > 0:
            networks = cls.get_neighbors(networks, neighbors=remaining_neighbors)
        return networks

    @classmethod
    def get_network_on_cursor(cls, region, view):
        network = None
        selection_functions = [
            lambda view, region: SelectionUtility.word(view, region),
            lambda view, region: SelectionUtility.left_word(view, region),
            lambda view, region: SelectionUtility.right_word(view, region),
            lambda view, region: SelectionUtility.left_word(view, region, repeat=2),
            lambda view, region: SelectionUtility.right_word(view, region, repeat=2),
            lambda view, region: SelectionUtility.right_word(
                view, SelectionUtility.left_word(view, region).begin(), repeat=2
            ),
        ]
        for index, selection_function in enumerate(selection_functions):
            selected = selection_function(view, region)
            network_region = view.substr(selected)
            current_network = cls.get(network_region)
            if current_network:
                    logger.debug('Selection function #{} found network {} in text "{}". '.format(
                        index + 1,
                        current_network,
                        network_region,
                    ))
                    if network is None:
                        network = current_network
                    elif current_network.network.prefixlen < network.network.prefixlen:
                        network = current_network
        return str(network) if network else ''

    @classmethod
    def masks(cls, interface):
        return [
            '/' + str(interface.network.prefixlen),
            str(interface.netmask),
            str(interface.hostmask),
        ]

    @classmethod
    def contains(cls, group, member):
        return int(group.network.network_address) <= int(member.network.network_address) and \
            int(group.network.broadcast_address) >= int(member.network.broadcast_address)

    @classmethod
    def clean(cls, network_text):
        for remove in cls.prefix_removals:
            network_text = network_text.replace(remove, '')
        network_text = network_text.strip()
        network_text = network_text.replace('  ', ' ')
        return network_text

    @classmethod
    def _get_from_re_match(cls, network_text):
        network = None

        match = ip.v4.network.search(network_text)
        if match:
            ip_address = match.group('ip')
            prefix_length = match.group('prefix_length')
            netmask = match.group('netmask')
            wildcard = match.group('wildcard')
            mask = prefix_length or netmask or wildcard
            try:
                if mask:
                    network = ipaddress.ip_interface('/'.join([ip_address, mask]))
                else:
                    network = ipaddress.ip_interface(ip_address)
            except ValueError:
                pass
            logger.debug('Network regexp match: "{}" from {}'.format(network, match.group()))
        else:
            match = ip.v4.host.search(network_text)
            if match:
                ip_address = match.group('ip')
                network = ipaddress.ip_interface(ip_address)
                logger.debug('Host regexp match: "{}" from {}'.format(network, match.group()))
                
        return network

    @classmethod
    def get(cls, network_text):
        network_text = cls.clean(network_text)
        # network_text = '/'.join(network_text.split())
        # logger.debug('bang: {}'.format(network_text))
        network = cls._get_from_re_match(network_text)
        # try:
        #     network = ipaddress.ip_interface(network_text)
        # except ValueError:
        #     network = None
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
