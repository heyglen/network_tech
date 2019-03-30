"""
Copyright 2019 Glen Harmon



"""

from collections import namedtuple
import ipaddress
import pathlib
import sys

import requests

from .factory import Parse

# installed_pacakges = str(pathlib.Path(__file__).parent.parent.parent)
# sys.path.append(installed_pacakges)

from network_tech.lib.utilities import cache


_URL = namedtuple('Url', 'ipv4 ipv6')(
    ipv4='https://www.iana.org/assignments/ipv4-address-space/ipv4-address-space.xml',
    ipv6='https://www.iana.org/assignments/ipv6-unicast-address-assignments/ipv6-unicast-address-assignments.xml',
)



class Iana:

    def __init__(self, file_cache_path=None):
        self._file_cache_path = file_cache_path
        self._get_cached = None

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


    def get_registrar(self, value):
        ip = ipaddress.ip_interface(value).network.network_address
        if value.version is 6:
            results = self._get_ipv6_reservations()
        elif value.version is 4:
            results = self._get_ipv4_reservations()
        value = None
        for result in results:
            if ip in result.prefix:
                value = result.rir
                break

        return value

    def _get(self, url):
        if self._get_cached is None:

            @cache.file(path=self._file_cache_path, expire_minutes=4320)
            def get_cached(url):
                response = self._session.get(url)
                response.raise_for_status()
                return response.content.decode('utf-8')

            self._get_cached = get_cached

        return self._get_cached(url)


    def _get_ipv4_reservations(self):
        content = self._get(_URL.ipv4)
        results = Parse.ipv4(content)
        return results

    def _get_ipv6_reservations(self):
        content = self._get(_URL.ipv6)
        results = Parse.ipv6(content)
        return results
