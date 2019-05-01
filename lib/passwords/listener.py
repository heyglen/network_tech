
# import functools

# import sublime
# import sublime_plugin

# from . import pw_type7
# # from . import pw_type5
# from .scopes import scopes


# def format_password(password, background_color='red'):
#     return """
#     <html>
#         <body id='network_tech'>
#             <style>
#                 html, body {{
#                     margin: 0px;
#                     padding: 0px;
#                     border: 0px;
#                 }}
#                 h3.password {{
#                     background-color: {1};
#                     color: white;
#                     padding: 5px;
#                 }}
#             </style>
#             <h3 class='password'>{0}</h3>
#         </body>
#     </html>
#     """.format(password, background_color)


# IN_PROGRESS = set()


# class PasswordDecryptViewListener(sublime_plugin.ViewEventListener):

#     def on_hover(self, point, hover_zone):
#         for scope_name in self.view.scope_name(point).split():
#             scope_name = scope_name.strip()
#             if scopes.type_prefix in scope_name:
#                 if hover_zone != sublime.HOVER_TEXT:
#                     self.view.hide_popup()
#                     return
                
#                 region = self.view.extract_scope(point)
#                 password = self.view.substr(region)
                
#                 background_color = 'black'
#                 decrypted_password = 'brute forcing password...'
#                 self._show_popup(region, decrypted_password)
#                 self._set_status(decrypted_password)

#                 if password not in IN_PROGRESS:
#                     IN_PROGRESS.add(password)
#                     if scope_name in scopes.type_7:
#                         self._set_status('Decoding {}'.format(password))
#                         decrypted_password = pw_type7.decode(password)
#                         background_color = 'red'
#                     elif scope_name in scopes.type_5:
#                         # self._set_status('Brute Forcing {}'.format(password))
#                         # decrypted_password = pw_type5.decode(password)
#                         # background_color = 'red'
#                         # if decrypted_password is None:
#                         #     decrypted_password = 'Brute force decode failed for {}'.format(password)
#                         #     background_color = 'green'
#                         decrypted_password = 'Use command pallet to decode: "Network Tech: Brute Force Type 5 Passwords"'
#                     else:
#                         decrypted_password = 'Unhandled password type'
#                         background_color = 'black'
#                     self._set_status('')
#                     IN_PROGRESS.remove(password)
    
#                     if isinstance(decrypted_password, bytes):
#                         decrypted_password = decrypted_password.decode('ascii')
    
#                     print('Cracking password {} done: {}'.format(password, decrypted_password))

#                 formatted_password = format_password(decrypted_password, background_color)
#                 self._show_popup(region, formatted_password)

#     def _set_status(self, message):
#         self.view.window().status_message(message)

#     def _show_popup(self, region, message):
#         if self.view.is_popup_visible():
#             self.view.update_popup(message)
#         else:
#             self.view.show_popup(
#                 message,
#                 flags=sublime.COOPERATE_WITH_AUTO_COMPLETE,
#                 location=region.begin(),
#             )


# class PasswordDecryptListener(sublime_plugin.EventListener):


#     def _cache_type_5_passwords(self, view):
#         password_hashes = set()
#         for scope in scopes.type_5:
#             for region in view.find_by_selector(scope):
#                 password_hash = view.substr(region)
#                 password_hashes.add(password_hash)


#         for password in password_hashes:
#             if password not in IN_PROGRESS:
#                 IN_PROGRESS.add(password)
#                 view.window().status_message('Brute Forcing {}'.format(password))
#                 sublime.set_timeout_async(
#                     functools.partial(pw_type5.decode, password),
#                     0
#                 )
#                 # pw_type5.decode(password)
#                 IN_PROGRESS.remove(password)

#     def on_modified_async(self, view):
#         self._cache_type_5_passwords(view)

#     def on_load_async(self, view):
#         self._cache_type_5_passwords(view)

#     def on_activated_async(self, view):
#         for window in sublime.windows():
#             window_view = window.active_view()
#             self._cache_type_5_passwords(window_view)

