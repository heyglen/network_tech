import logging

import sublime
import sublime_plugin

from .variables import SYNTAX, DETECT_SYNTAX

logger = logging.getLogger('network_tech.detect_syntax.syntax_detection_listener')


class AutoSyntaxDetection(sublime_plugin.ViewEventListener):
    def on_modified_async(self):
        if self.is_plain_text and self.is_cisco:
            if self.is_nxos:
                self.view.set_syntax_file(SYNTAX.nxos)
            elif self.is_asa:
                self.view.set_syntax_file(SYNTAX.asa)
            elif self.is_ios:
                self.view.set_syntax_file(SYNTAX.ios)
            elif self.is_ace:
                self.view.set_syntax_file(SYNTAX.ace)

    @property
    def is_plain_text(self):
        return self.view.scope_name(0).strip() == 'text.plain'

    def is_cisco(self):
        for evidence in DETECT_SYNTAX.cisco:
            if self.view.find(evidence, 0):
                return True
        return False

    @property
    def is_asa(self):
        return self._syntax_detection(DETECT_SYNTAX.asa, 'Cisco ASA detected')

    @property
    def is_nxos(self):
        return self._syntax_detection(DETECT_SYNTAX.nxos, 'Cisco NXOS detected')

    @property
    def is_ace(self):
        return self._syntax_detection(DETECT_SYNTAX.ace, 'Cisco ACE detected')

    @property
    def is_ios(self):
        return self._syntax_detection(DETECT_SYNTAX.ios, 'Cisco IOS detected')

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
