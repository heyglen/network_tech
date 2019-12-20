# Copyright 2017 Glen Harmon

import logging

import sublime_plugin

# from .scopes import scopes
from . import mac

logger = logging.getLogger('network_tech.search.network')


SCOPE_PREFIX = 'text.network'

MAC_FORMATS = ['Colon', 'Dot', 'Dash']
MAC_FORMAT_FN = {
    'colon': 'colon_format_mac',
    'dot': 'dot_format_mac',
    'dash': 'dash_format_mac',
}


def _run(edit, view, fn):
    for region in view.sel():
        address = view.substr(region)
        view.replace(edit, region, fn(address))


class DashFormatMacCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        _run(edit, self.view, mac.dash)


class ColonFormatMacCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        _run(edit, self.view, mac.colon)


class DotFormatMacCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        _run(edit, self.view, mac.dot)


class FormatMacCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        if not self.view.sel():
            return

        def _on_done(index):
            if index == -1:
                return

            format_choice = MAC_FORMATS[index].lower()
            command = MAC_FORMAT_FN[format_choice.lower()]
            self.view.run_command(command, {})

        window = self.view.window()
        window.show_quick_panel(
            MAC_FORMATS,
            _on_done,
        )

