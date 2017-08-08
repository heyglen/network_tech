import re
import ipaddress
import logging

import sublime
import sublime_plugin

logger = logging.getLogger('net_tech')
logger.handlers = []
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
                (?:
                    (?:
                        (?:
                            (?:host)|
                            (?:range)
                        )
                        \s+
                    )?
                    (?P<ip>
                        (?:(?:\d{1,3}\.){3}\d{1,3})
                    )
                )
                (?:
                    (?:/(?P<prefix_length>\d{1,2}))|
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
        'network':  re.compile(
                    r"""
                    (?xi)
                    (?:
                        (?P<ip>
                            (?:(?:\d{1,3}\.){3}\d{1,3})
                        )
                        (?:
                            (?:/(?P<prefix_length>\d{1,2}))|
                            (?:
                                \s+
                                (?:
                                    (?:mask\s+)?
                                    (?P<netmask>(\d{1,3}\.){3}\d{1,3})
                                )
                            )
                        )
                    )
                    """
        ),
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


class Html:

    @classmethod
    def unordered_list(cls, items):
        return cls._tag(
            'ul',
            content=[cls.li(i) for i in items],
            style='list-style-type:none'
        )

    @classmethod
    def _tag(cls, tag, content=None, style=None):
        style = ' style="{}"'.format(style or '')
        if isinstance(content, list):
            content = ''.join(content)
        content = str(content or '')
        return '<{}{}>{}</{}>'.format(tag, style, content, tag)

for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'hr', 'div', 'span', 'li']:
    setattr(
        Html,
        tag,
        classmethod(lambda cls, text='': cls._tag(tag, content=text))
    )

class SelectionUtility:

    @classmethod
    def _get_word_on_cursor(cls, view, point):
        if isinstance(point, sublime.Region):
            point = point.end()
        return view.word(point)

    @classmethod
    def _get_line_on_cursor(cls, view, point):
        if isinstance(point, sublime.Region):
            point = point.end()
        return view.line(point)

    @classmethod
    def left_word(cls, view, region, repeat=1):
        return cls._expand_words(
            view,
            region,
            classes=sublime.CLASS_WORD_END,
            repeat=repeat,
            forward=False,
        )

    @classmethod
    def right_word(cls, view, region, repeat=1):
        return cls._expand_words(
            view,
            region,
            classes=sublime.CLASS_WORD_START,
            repeat=repeat,
            forward=True,
        )

    @classmethod
    def _expand_words(cls, view, region, classes, repeat=1, forward=True):
        word = cls._get_word_on_cursor(view, region)
        line = cls._get_line_on_cursor(view, region)
        current_word = word
        for expand in range(repeat):
            next_word_end = view.find_by_class(
                current_word.end() if forward else current_word.begin(),
                forward=forward,
                classes=classes
            )
            next_word = cls._get_word_on_cursor(view, next_word_end)
            if line == cls._get_line_on_cursor(view, next_word):
                current_word = cls._get_word_on_cursor(view, next_word_end)

        start = word.begin() if forward else current_word.begin()
        end = current_word.end() if forward else word.end()
        return sublime.Region(start, end)

class Network:
    prefix_removals = [
        'host',
        'mask',
        'range'
    ]

    @classmethod
    def get_network_on_cursor(cls, region, view):
        network = None
        selection_functions = [
            lambda view, region: SelectionUtility.left_word(view, region),
            lambda view, region: SelectionUtility.right_word(view, region),
            lambda view, region: SelectionUtility.left_word(view, region, repeat=2),
            lambda view, region: SelectionUtility.right_word(view, region, repeat=2),
            lambda view, region: SelectionUtility.right_word(view, SelectionUtility.left_word(view, region).begin(), repeat=2),
        ]
        for index, selection_function in enumerate(selection_functions):
            selected = selection_function(view, region)
            network_region = view.substr(selected)
            logger.debug('Possible network under cursor: #{} {}'.format(index, network_region))
            current_network = cls.get(network_region)
            if current_network:
                if network is None or current_network.prefixlen < network.prefixlen:
                    network = current_network
        return str(network)


    @classmethod
    def masks(cls, interface):
        return [
            '/' + str(interface.network.prefixlen),
            str(interface.netmask),
            str(interface.hostmask),
        ]

    @classmethod
    def contains(cls, group, member):
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

                    cleaned_region = Network.clean_region(self.view, found_region)
                    network_re_match = self.view.substr(cleaned_region)
                    logger.debug('Network RE match {}'.format(network_re_match))
                    found_network = Network.get(network_re_match)

                    if Network.contains(search_network, found_network):
                        self.view.sel().clear()
                        self.view.show_at_center(cleaned_region.begin())
                        logger.debug('Found region {} {}'.format(
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
        # network = Network.get(under_cursor)
        default_search = under_cursor if under_cursor else ''
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
        default_search = Network.get_network_on_cursor(self.view.sel()[0], self.view)
        default_search = default_search if ip.v4.network.search(default_search) else ''
        self._find_input_panel(network=default_search)


class NetworkAutoCompleteListener(sublime_plugin.ViewEventListener):
    # def on_query_completions(self, prefix, locations):
    def on_modified_async(self):
        for region in self.view.sel():
            match_text = Network.get_network_on_cursor(region, self.view)
            match = ip.v4.network.search(match_text)
            if match:
                ip_address = match.group('ip')
                prefix_length = match.group('prefix_length')
                netmask = match.group('netmask')
                if prefix_length or netmask:
                    logger.debug('Network Regexp Match: {}'.format(match.groups()))
                    network = ipaddress.ip_interface(
                        '/'.join([ip_address, (prefix_length or netmask)])
                    )
                    if network:
                        content = ''.join([
                            Html.span('Network: ' + str(network.network.network_address)),
                            Html.span('Broadcast: ' + str(network.network.broadcast_address)),
                            Html.span('Masks:'),
                            Html.unordered_list(Network.masks(network)),
                        ])
                        if self.view.is_popup_visible():
                            self.view.update_popup(content)
                        else:
                            self.view.show_popup(
                                content,
                                flags=sublime.COOPERATE_WITH_AUTO_COMPLETE
                            )
