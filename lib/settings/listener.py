# Copyright 2017 Glen Harmon

import logging

import sublime
import sublime_plugin

logger = logging.getLogger('network_tech.settings.listener')


STATUS_KEY = 'Network Tech'
SETTINGS_FILE_NAME = 'Network Tech.sublime-settings'
NETWORK_INFO_ON_HOVER_SETTING_NAME = 'network_info_on_hover'

class ToggleNetworkInfoOnHoverCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        settings = sublime.load_settings(SETTINGS_FILE_NAME)
        network_info_on_hover = settings.get(NETWORK_INFO_ON_HOVER_SETTING_NAME, True)
        settings.set(NETWORK_INFO_ON_HOVER_SETTING_NAME, not network_info_on_hover)
        sublime.save_settings(SETTINGS_FILE_NAME)

        setting_status = 'ON' if not network_info_on_hover else 'OFF'
        set_status = 'Network Info Popup: {}'.format(setting_status)

        def clear_status():
            current_status = self.view.get_status(STATUS_KEY)
            if set_status == current_status:
                self.view.erase_status(STATUS_KEY)

        self.view.set_status(STATUS_KEY, set_status)
        sublime.set_timeout_async(clear_status, 4000)