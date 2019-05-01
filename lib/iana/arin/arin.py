# Copyright 2019 Glen Harmon

import ipaddress
import contextlib

# Using 3rd Party Libraries in Sublime Text
# https://github.com/packagecontrol/requests
import requests

# from .record import Record


BASE_URL = 'http://whois.arin.net/rest'


class Arin:

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
            self._session_ = session
        return self._session_


    def _clean_input(self, value):
        with contextlib.suppress(ValueError):
            return ipaddress.ip_address(value)
        with contextlib.suppress(ValueError):
            return ipaddress.ip_interface(value).network
        return value

    def search(self, value):
        value = self._clean_input(value)
        path = 'cidr'
        if isinstance(value, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            path = 'ip'
        # More means that more specific registrations are returned 
        # Could also use 'less' for supernets
        path_prefix = 'more'
        response = self._session.get(
            '/'.join([BASE_URL, path, path_prefix])
        )
        response.raise_for_status()
        info = self._parse_response(response)
        return info
        # return self._format_response(info)

#     def _parse_response(self, response):
#         body = response.json()
#         info = dict()

#         interesting = [
#             'registrationDate',
#         ]

#         record = Record()

#         arin_object = body.get('net', dict())

#         prefix_name = arin_object.get('name')

#         created = arin_object.get('registrationDate')
#         modified = arin_object.get('updateDate')
#         handle = arin_object.get('handle')        
        
#         organization = arin_object.get('orgRef')
#         organization_name = organization.get('@name')
#         organization_handle = organization.get('@handle')
        
#         network_block = arin_object.get('netBlocks', dict()).get('netBlock', dict())
#         start_address = network_block.get('startAddress'),
#         end_address = network_block.get('endAddress'),
#         prefix_length = network_block.get('cidrLength'),
#         prefix_type = network_block.get('type'),
#         description = network_block.get('description'),

#         network = ipaddress.ip_interface('{}/{}'.format(start_address, prefix_length)).network
#         if start_address != str(network.network_address) or end_address != str(network.broadcast_address):
#             network = '{}/{} - {}/{}'.format(
#                 start_address,
#                 prefix_length,
#                 end_address,
#                 prefix_length,
#             )
#         else:
#             network = str(network)

#         return {
#             'arin':[
#                 {
#                     'name': prefix_name,
#                     'description': description,
#                     'type': prefix_type,
#                     'handle': handle,
#                     'created': created,
#                     'modified': modified,
#                     'headers': headers,
#                     'attributes': attributes,
#                 }
#             ]
#         }

        
#     def _format_response(self, info):
#         text = ''
#         for source, records in info.items():
#             text += '{}\n'.format(source.upper())
#             for record in records:
#                 iana_type = record.get('type')
#                 text += '\t{}\n'.format(iana_type)
#                 for name, value in record.get('headers', dict()).items():
#                     text += '\t\t{} {}\n'.format(name, value)
#                 for name, value in record.get('attributes', dict()).items():
#                     text += '\t\t\t{} {}\n'.format(name, value)
#                 text.strip('\n')
#         return text

# if __name__ == '__main__':
#     ripe = Ripe()
#     text = ripe.search('217.16.100.0/24')
#     # text = json.dumps(response.json(), indent=4, sort_keys=True)
#     print(text)