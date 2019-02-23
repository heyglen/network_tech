# Copyright 2019 Glen Harmon

import datetime
import ipaddress



def default_attribute_value_cleaner(value):
    return value


def get_datetime_object(timestamp):
    datetime_object = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    # Remove Microseconds
    datetime_object = datetime_object.replace(microsecond=0)
    timestamp = datetime_object.isoformat(' ').rstrip('Z').replace('+', ' +')
    return timestamp
    # Convert to local timezone
    # datetime_object = datetime_object.replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())
    # return datetime_object.isoformat(' ').rstrip('Z').replace('+', ' +')


def get_ip_address(ip):
    return ipaddress.ip_address(ip)


def get_network(network):
    return ipaddress.ip_interface(network).network


def get_asn(asn):
    return int(asn.replace('AS', ''))


CLEAN_TYPE_ATTRIBUTE_FN_BASE = {
    'created': get_datetime_object,
    'last-modified': get_datetime_object,
    'modified': get_datetime_object,
}

CLEAN_TYPE_ATTRIBUTE_FN = {
    'inetnum': {},
    'inet6num': {},
    'route': {
        'origin': get_asn,
        'route': get_network,    
        'aggr-bndry': get_asn,    
    },
    'route6': {
        'origin': get_asn,
        'route6': get_network,    
        'aggr-bndry': get_asn,    
    },
    'as-block': {},
    'irt': {},
    'key-cert': {},
    'mntner': {},
    'organisation': {},
    'person': {},
    'poem': {},
    'poetic-form': {},
    'role': {},
}

for _, value in CLEAN_TYPE_ATTRIBUTE_FN.items():
    value.update(CLEAN_TYPE_ATTRIBUTE_FN_BASE)


def clean_attribute_value(ripe_type, attribute, value):
    attribute_cleaning_functions = CLEAN_TYPE_ATTRIBUTE_FN.get(ripe_type, dict())
    cleaner_fn = attribute_cleaning_functions.get(attribute, default_attribute_value_cleaner)
    return cleaner_fn(value)
