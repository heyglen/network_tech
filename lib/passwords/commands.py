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

def async_decode_single_password(pre_command_selection, pre_command_visible_region, view, passwords, index):
    """ Calls decode_single_password asyncronously so the UI does not block"""
    sublime.set_timeout_async(
        functools.partial(
            decode_single_password,
            pre_command_selection,
            pre_command_visible_region,
            view,
            passwords,
            index
        ),
        0
    )

def decode_single_password(pre_command_selection, pre_command_visible_region, view, passwords, index):
    if index is -1:
        # Excape pressed
        # Return selections to previous state
        selection = view.sel()
        selection.clear()
        selection.add_all(pre_command_selection)
        view.show_at_center(pre_command_visible_region)
        return

    password = passwords[index]
    encoded_password = password.encoded
    try:
        view.window().status_message('Network Tech: Decoding password...')
        decoded_password = password.decoder(password.encoded)
        view.window().status_message('')
    except InvalidPassword as e:
        sublime.message_dialog(str(e))
        return 


    if isinstance(decoded_password, bytes):
        decoded_password = decoded_password.decode('ascii')

    if decoded_password is not None:
        options = [
            'Display password',
            'Copy password to clipboard (Clears in 10 seconds)',
        ]

        view.window().show_quick_panel(
            options,
            functools.partial(result_handler, view, encoded_password, decoded_password),
        )
    else:
        sublime.message_dialog('Unable to brute force the password "{}"'.format(encoded_password))


def jump_to_region(pre_command_selection, pre_command_visible_region, view, passwords, index):
    if index is -1:
        # Excape pressed
        # Return selections to previous state
        selection = view.sel()
        selection.clear()
        selection.add_all(pre_command_selection)
        view.show_at_center(pre_command_visible_region)
        return
    region = passwords[index].region
    selection = view.sel()
    view.show_at_center(region)
    selection.clear()
    selection.add(region)
    

class DecodePasswordCommand(sublime_plugin.TextCommand):

    def decode(self):
            
        PasswordType = namedtuple('PasswordType', 'region decoder encoded line')

        # Collect all passwords
        scopes_to_decoder = [
            (scopes.type_5, pw_type5.decode),
            (scopes.type_7, pw_type7.decode),
        ]

        passwords = list()
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

        # Get the closest region as the default selected password
        selection = self.view.sel()
        selected_index = 0
        if len(selection) is 1:
            selected_region = selection[0]
            best_distance = 10000
            closest_region = None
            for index, password in enumerate(passwords):
                if selected_region.intersects(password.region):
                    selected_index = index
                    break
                else:

                    if (password.region.begin() - selected_region.begin()) < best_distance:
                        best_distance = abs(password.region.begin() - selected_region.begin())
                        closest_region = password.region
                        selected_index = index
                    elif (password.region.end() - selected_region.end()) < best_distance:
                        best_distance = abs(password.region.end() - selected_region.end())
                        closest_region = password.region
                        selected_index = index

                if closest_region is None:
                    closest_region = password.region

        # Save the current selections in case password selection is cancelled
        pre_command_selection = [sublime.Region(r.a, r.b) for r in self.view.sel()]
        pre_command_visible_region = self.view.visible_region()

        self.view.window().show_quick_panel(
            [password.line for password in passwords],
            functools.partial(async_decode_single_password, pre_command_selection, pre_command_visible_region, self.view, passwords),
            0,
            selected_index,
            functools.partial(jump_to_region, pre_command_selection, pre_command_visible_region, self.view, passwords)
        )

    def run(self, edit):
        self.decode()

