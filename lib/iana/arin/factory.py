# Copyright 2019 Glen Harmon

import contextlib
import ipaddress
import functools
import re


def rsetattr(obj, attr, value):
    attrs = attr.split('.')
    setattr(functools.reduce(getattr, attrs[:-1], obj), attrs[-1], value)


class RouteRecordParser:

    @classmethod
    def ripe(cls, response):
        route = RouteRecord()
        body = response.json()
        type_filter = ['route']
        
        attribute_map = {
            'route': 'prefix.network',
            'descr': 'description',
            'origin': 'prefix.autonomous_system',
            'mnt-by': 'maintainer.name',
            'source': 'source',
            'created': 'created',
            'last-modified': 'modified',
        }

        for ripe_object in body.get('objects', dict()).get('object', list()):
            ripe_type = ripe_object.get('type')
            if ripe_type not in type_filter:
                continue
            primary_keys = ripe_object.get('primary-key', dict()).get('attribute', list())
            attributes = ripe_object.get('attributes', dict()).get('attribute', list())


            for attribute in (primary_keys + attributes):
                if attribute in attribute_map:
                    continue

                name = attribute['name']
                value = attribute['value']

                rsetattr(
                    route,
                    attribute_map[name],
                    value
                )
        return route


class NetworkRecordParser:

    @classmethod
    def ripe(cls, response):
        record = NetworkRecord()
        
        body = response.json()
        type_filter = ['inetnum']
        
        attribute_map = {
            'inetnum': 'handle',
            'netname': 'name',
            'descr': 'description',
            'country': 'country',
            'status': 'prefix_type',
            'mnt-by': 'maintainer.name',
            'source': 'source',
        }

        for ripe_object in body.get('objects', dict()).get('object', list()):
            ripe_type = ripe_object.get('type')
            if ripe_type not in type_filter:
                continue

            primary_keys = ripe_object.get('primary-key', dict()).get('attribute', list())
            attributes = ripe_object.get('attributes', dict()).get('attribute', list())


            for attribute in (primary_keys + attributes):
                if attribute in attribute_map:
                    continue

                name = attribute['name']
                value = attribute['value']

                rsetattr(
                    record,
                    attribute_map[name],
                    value
                )
        return record


    @classmethod
    def arin(cls, response):
        record = NetworkRecord()

        body = response.json()

        arin_object = body.get('net', dict())
        record.source = 'arin'
        record.name = arin_object.get('name')

        record.created = arin_object.get('registrationDate')
        record.modified = arin_object.get('updateDate')
        record.handle = arin_object.get('handle')        
        
        organization = arin_object.get('orgRef')
        record.organization.name = organization.get('@name')
        record.organization.handle = organization.get('@handle')
        

        network_block = arin_object.get('netBlocks', dict()).get('netBlock', dict())
        
        record.description = network_block.get('description'),
        record.network.start_allocation = network_block.get('startAddress'),
        record.network.end_allocation = network_block.get('endAddress'),
        record.network.prefix_length = network_block.get('cidrLength'),
        
        record.prefix_type = network_block.get('type'),

        return record


class Prefix:
    def __init__(self):
        self.start_allocation = None
        self.end_allocation = None
        self.prefix_length = None
        self._network = None
        self._autonomous_system = None

    @property
    def network(self):        
        return self._network

    @network.setter
    def network(self, value):
        with contextlib.suppress(ValueError):
            self.network = ipaddress.ip_interface(value).network
            return
        with contextlib.suppress(ValueError):
            self._network_address = ipaddress.ip_address(value)
            return
        raise ValueError('Invalid network {}'.format(value))

    @property
    def autonomous_system(self):        
        return self._network

    @autonomous_system.setter
    def autonomous_system(self, value):
        if not re.match(r'^AS\d+$', value):
            raise ValueError('Invalid Autonomous System {}'.format(value))
        self._autonomous_system = int(value[2:])


class OrganizationRecord:
    def __init__(self):
        self.name = None
        self.handle = None


class MaintainerRecord:
    def __init__(self):
        self.name = None


class NetworkRecord:
    def __init__(self):
        self.source = None
        self.prefix_name = None
        self.handle = None
        self.description = None
        self.prefix_type = None
        self.created = None
        self.modified = None
        self.country = None
        self.attributes = dict()
        self.headers = dict()

        self.prefix = Prefix()
        self.organization = OrganizationRecord()
        self.maintainer = MaintainerRecord()


class RouteRecord:

    def __init__(self):
        self.prefix = Prefix()
