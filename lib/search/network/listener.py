# Copyright 2017 Glen Harmon

import logging
import functools

import sublime
import sublime_plugin

# from .scopes import scopes
from .network import Network
from .variables import sublime_ip, ip
from .html_helper import Html

logger = logging.getLogger('network_tech.search.network')


SCOPE_PREFIX = 'text.network'


class NetworkInfoListener(sublime_plugin.ViewEventListener):
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
        if point is None or not self.view.scope_name(point).startswith(SCOPE_PREFIX):
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
                    self._update_popup(content, location)

                self._loading_popup(
                    location,
                    content,
                    functools.partial(Network.rir, network),
                    'Getting RIR...'
                )
            # Match only the first
            break

    def _loading_popup(self, location, content, callback, loading_message='loading...'):

        def _update(self, location, content, callback, loading_message):
            loading_content = content + Html.div(loading_message)
            self._update_popup(loading_content, location)

            output = callback()
            self._update_popup(content + output, location)

        sublime.set_timeout_async(
            functools.partial(_update, self, location, content, callback, loading_message),
            0,
        )

    def _update_popup(self, content, location):
        if content:
            if self.view.is_popup_visible():
                self.view.update_popup(content)
            else:
                self.view.show_popup(
                    content,
                    flags=sublime.COOPERATE_WITH_AUTO_COMPLETE,
                    location=location,
                )

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


# class NetworkCompletionListener(sublime_plugin.ViewEventListener):

#     def on_query_completions(self, prefix, locations):
#         for point in locations:
#             if self.view.match_selector(point, scopes.ipv4.incomplete.ip):
#                 print('ding')
#                 print(prefix)
#         return