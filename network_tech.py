# Copyright 2017 Glen Harmon

import logging

import sublime
import sublime_plugin

from .lib.dot_dict import DotDict
from .lib.ip_regex import sublime_ip, ip
from .lib.network import Network


logger = logging.getLogger('net_tech')
logger.handlers = []

SCOPE_PREFIX = 'text.network'

settings = sublime.load_settings('network_tech.sublime-settings')

log_level = settings.get('log_level', 'warning') or 'warning'
logger.setLevel(
    getattr(logging, log_level.upper())
)


SYNTAX = DotDict({
    'asa': 'Packages/network_tech/cisco-asa.sublime-syntax',
    'ace': 'Packages/network_tech/cisco-ace.sublime-syntax',
    'ios': 'Packages/network_tech/cisco-ios.sublime-syntax',
    'nxos': 'Packages/network_tech/cisco-nxos.sublime-syntax',
})

detect_syntax = DotDict({
    'cisco': [
        '^! Last configuration change at',
        '^!Command: show ',
        '^: Hardware:\s+ASA\d+',
        '^ASA Version \d+\.\d+',
        '^Building configuration...$',
        '^Current configuration : \d+ bytes$',
        '^Generating configuration....',
    ],
    'asa': [
        '^ASA Version \d+\.\d+',
        '^: Hardware:\s+ASA\d+',
        '^\s*security-level \d+$',
        '^\s*nameif \S+$',
        '^\s*access-list cached ACL log flows:',
        '^\s*route\s+\S+\d+',
        '^\s*fragment chain \d+ \S+$',
        '^\s*asdm image \S+$',
        '^\s*same-security-traffic',
    ],
    'nxos': [
        '^!Command: show ',
        '^\s*feature \S+',
        '^\s*vrf context \S+',
    ],
    'ace': [
        '^Generating configuration....',
    ],
    'ios': [
        '^\s*ip classless$',
        '^\s*ip subnet-zero$',
        '^\s*redundancy$',
        '^\s*mode sso$',
        '^\s*main-cpu$',
        '^\s*auto-sync standard$',
        '^\s*spanning-tree extend system-id$',
        '^\s*vlan internal allocation policy ascending$',
        '^Current configuration : \d+ bytes$',
        '^Building configuration...$',
        '^\s*access-list \d{2,3} ((?:permit)|(?:deny))',
    ],
})


class SearchHistory(list):
    @property
    def last(self):
        last = None
        if self:
            last = self[0]
        return last


class FindSubnetCommand(sublime_plugin.TextCommand):

    def get_network(self, network, find_all=False):
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

                    cleaned_region = Network.clean_region(self.view, found_region)
                    network_re_match = self.view.substr(cleaned_region)
                    logger.debug('Network RE match {}'.format(network_re_match))
                    found_network = Network.get(network_re_match)
                    logger.debug('Network Object {} generated'.format(found_network))
                    if found_network and Network.contains(search_network, found_network):
                        self.view.sel().clear()
                        self.view.show_at_center(cleaned_region.begin())
                        logger.debug('Network found in {} {}'.format(
                            cleaned_region.begin(),
                            cleaned_region.end())
                        )
                        self.view.sel().add(sublime.Region(
                            cleaned_region.begin(),
                            cleaned_region.end()
                        ))
                        break
                    cursor = cleaned_region.end()

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
        under_cursor = Network.get_network_on_cursor(self.view.sel()[0], self.view)
        default_search = under_cursor if under_cursor else ''
        self._find_input_panel(network=default_search)


class FindAllSubnetsCommand(sublime_plugin.TextCommand):

    def get_network(self, networks, find_all=False):
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

    def _find_input_panel(self, network=''):
        self.view.window().show_input_panel(
            caption='Find all Network(s) - comma seperated',
            initial_text=network,
            on_done=self.get_network,
            on_change=None,
            on_cancel=None
        )

    def run(self, edit):
        default_search = Network.get_network_on_cursor(self.view.sel()[0], self.view)
        default_search = default_search if ip.v4.network.search(default_search) else ''
        self._find_input_panel(network=default_search)


class NetworkAutoCompleteListener(sublime_plugin.ViewEventListener):
    def on_hover(self, point, hover_zone):
        if not self.view.scope_name(point).startswith(SCOPE_PREFIX):
            return
        if hover_zone == sublime.HOVER_TEXT:
            if self.view.is_popup_visible():
                self.view.hide_popup()
            self.network_info(point=point, location=point)
        else:
            self.view.hide_popup()

    def on_modified_async(self):
        self.network_info()

    def network_info(self, point=None, location=None):
        if not self.view.scope_name(point).startswith(SCOPE_PREFIX):
            return
        regions = self.view.sel() if point is None else [sublime.Region(point, point)]
        location = regions[0].end() if location is None else location

        for region in regions:
            if not self.view.match_selector(region.end(), 'text.network'):
                continue
            match_text = Network.get_network_on_cursor(region, self.view)
            network = Network.get(match_text)
            if network:
                content = Network.info(network)
                if content:
                    if self.view.is_popup_visible():
                        self.view.update_popup(content)
                    else:
                        self.view.show_popup(
                            content,
                            flags=sublime.COOPERATE_WITH_AUTO_COMPLETE,
                            location=location,
                        )
            # Match only the first
            break


class AutoSyntaxDetection(sublime_plugin.ViewEventListener):
    def on_modified_async(self):
        if self.is_plain_text and self.is_cisco:
            if self.is_asa:
                self.view.set_syntax_file(SYNTAX.asa)
            elif self.is_ios:
                self.view.set_syntax_file(SYNTAX.ios)
            elif self.is_nxos:
                self.view.set_syntax_file(SYNTAX.nxos)
            elif self.is_ace:
                self.view.set_syntax_file(SYNTAX.ace)

    @property
    def is_plain_text(self):
        return self.view.scope_name(0).strip() == 'text.plain'

    def is_cisco(self):
        for evidence in detect_syntax.cisco:
            if self.view.find(evidence, 0):
                return True
        return False

    @property
    def is_asa(self):
        return self._syntax_detection(detect_syntax.asa, 'Cisco ASA detected')

    @property
    def is_nxos(self):
        return self._syntax_detection(detect_syntax.nxos, 'Cisco NXOS detected')

    @property
    def is_ace(self):
        return self._syntax_detection(detect_syntax.ace, 'Cisco ACE detected')

    @property
    def is_ios(self):
        return self._syntax_detection(detect_syntax.ios, 'Cisco IOS detected')

    def _syntax_detection(self, syntax_list, message, status_update=True):
        for evidence in syntax_list:
            if self.view.find(evidence, 0):
                if status_update:
                    self.view.erase_status('Network Tech')
                    self.view.set_status('Network Tech', message)
                    sublime.set_timeout(
                        (lambda: self.view.erase_status('Network Tech')),
                        3000
                    )
                logger.debug(message)
                return True
        return False
