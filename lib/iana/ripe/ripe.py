# Copyright 2019 Glen Harmon

import ipaddress
import contextlib
import functools

# Using 3rd Party Libraries in Sublime Text
# https://github.com/packagecontrol/requests
import requests

from .factory import build, get_sub_objects


_BASE_URL = 'https://rest.db.ripe.net/search'


class Ripe:

    def __init__(self):
        pass

    @property
    def _session(self):
        if not hasattr(self, '_session_'):
            session = requests.Session(
            )
            session.headers.update({
                'Accept': 'application/json'
            })
            self._session_ripe = session
        return self._session_ripe


    def _clean_input(self, value):
        with contextlib.suppress(ValueError):
            return str(ipaddress.ip_interface(value).network)
        return value

    @functools.lru_cache()
    def search(self, value, type_=None, recurse=2):
        value = self._clean_input(value)
        params = {
            'query-string': value,
        }
        if type_ is not None:
            params['type-filter'] = type_
        response = self._session.get(
            _BASE_URL,
            params=params,
        )
        response.raise_for_status()
        results = build(response)

        if recurse:
            known = {(o.type_, o.handle) for o in results}
            for type_, handle in get_sub_objects(response):
                key = (type_, handle)
                if key not in known:
                    known.add(key)
                    for new_object in self.search(handle, type_=type_, recurse=recurse - 1):
                        key = (new_object.type_, new_object.handle)
                        if key not in known:
                            known.add(key)
                            results.append(new_object)
        
        return results