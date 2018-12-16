import functools
from collections import namedtuple

import sublime
import sublime_plugin

from . import pw_type5
from . import pw_type7
from .scopes import scopes
from ..exceptions import InvalidPassword


IN_PROGRESS = set()
RESULTS = namedtuple('Results', 'cancel display clipboard')(
    cancel=-1,
    display=0,
    clipboard=1,
)


def decode(view, message, password):
    view.window().status_message(message)
    if password not in IN_PROGRESS:
        IN_PROGRESS.add(password)
        pw_type5.decode(password)
        IN_PROGRESS.remove(password)
    view.window().status_message('')


def clear_clipboard(view, password):
    if sublime.get_clipboard() == password:
        sublime.set_clipboard('')
        view.window().status_message('Network Tech: Password cleared from clipboard')


def result_handler(view, encoded_password, decoded_password, index):
    if index is RESULTS.cancel:
        return
    elif index is RESULTS.display:
        message = 'Encoded: {}\nDecoded: {}'.format(encoded_password, decoded_password)
        sublime.message_dialog(message)
    elif index is RESULTS.clipboard:
        sublime.set_clipboard(decoded_password)
        sublime.set_timeout_async(
            functools.partial(clear_clipboard, view, decoded_password),
            10000
        )

def async_decode_single_password(view, passwords, index):
    """ Calls decode_single_password asyncronously so the UI does not block"""
    sublime.set_timeout_async(
        functools.partial(
            decode_single_password,
            view,
            passwords,
            index
        ),
        0
    )

def decode_single_password(view, passwords, index):
    if index is -1:
        return

    password = passwords[index]
    encoded_password = password.encoded
    try:
        decoded_password = password.decoder(password.encoded)
    except InvalidPassword as e:
        sublime.message_dialog(str(e))
        return 


    if isinstance(decoded_password, bytes):
        decoded_password = decoded_password.decode('ascii')

    if decoded_password is not None:
        options = [
            'Display password',
            'Copy password to clipboard for 10 seconds.',
        ]

        view.window().show_quick_panel(
            options,
            functools.partial(result_handler, view, encoded_password, decoded_password),
        )
    else:
        sublime.message_dialog('Unable to brute force decode the password "{}"'.format(encoded_password))


def jump_to_region(view, passwords, index):
    if index is -1:
        return
    region = passwords[index].region
    selection = view.sel()
    view.show_at_center(region)
    selection.clear()
    selection.add(region)
    

class DecodePasswordCommand(sublime_plugin.TextCommand):

    def decode(self):

            
        PasswordType = namedtuple('PasswordType', 'region decoder encoded line')
        passwords = list()

        scopes_to_decoder = [
            (scopes.type_5, pw_type5.decode),
            (scopes.type_7, pw_type7.decode),
        ]

        for type_scopes, decoder in scopes_to_decoder:
            for scope in type_scopes:
                for region in self.view.find_by_selector(scope):
                    encoded_password = self.view.substr(region)
                    password = PasswordType(
                        region=region,
                        decoder=decoder,
                        encoded=encoded_password,
                        line=self.view.substr(self.view.line(region)).strip(),
                    )
                    passwords.append(password)


        passwords = sorted(passwords, key=lambda password: password.region.begin())

        selection = self.view.sel()
        selected_index = 0
        if len(selection) is 1:
            region = selection[0]
            for index, password in enumerate(passwords):
                if region.intersects(password.region):
                    selected_index = index
                    break

        self.view.window().show_quick_panel(
            [password.line for password in passwords],
            functools.partial(async_decode_single_password, self.view, passwords),
            0,
            selected_index,
            functools.partial(jump_to_region, self.view, passwords)
        )

    def run(self, edit):
        self.decode()

