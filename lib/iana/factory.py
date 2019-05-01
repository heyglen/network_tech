"""
Copyright 2019 Glen Harmon



"""


from io import StringIO
import ipaddress
from xml.etree import ElementTree


from .objects import Ipv4Record, Ipv6Record


def _strip_namespaces(xml):
    it = ElementTree.iterparse(StringIO(xml))
    for _, el in it:
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
    return it.root


def _clean_ipv4_prefix(prefix):
    ip, prefix_length = prefix.split('/')
    octets = ip.split('.')
    for _ in (range(4 - len(octets))):
        octets.append('0')
    octets = [str(int(i)) for i in octets]
    return ipaddress.ip_network('{}/{}'.format(
            '.'.join(octets),
            prefix_length
        ))


class Parse:

    @classmethod
    def ipv4(cls, content):
        tree = _strip_namespaces(content)
        reservations = list()
        for record in tree.findall("./record"):
            instance = Ipv4Record()

            for item in record.iter():
                if hasattr(instance, item.tag):
                    value = item.text
                    if item.tag == 'prefix':
                        value = _clean_ipv4_prefix(value)
                    setattr(instance, item.tag, value)                    
            reservations.append(instance)
        return reservations

    @classmethod
    def ipv6(cls, content):
        tree = _strip_namespaces(content)
        reservations = list()
        for record in tree.findall("./record"):
            instance = Ipv6Record()
            for item in record.iter():
                if hasattr(instance, item.tag):
                    value = item.text
                    if item.tag == 'prefix':
                        value = ipaddress.ip_network(value)
                    setattr(instance, item.tag, value)                    
            reservations.append(instance)
        return reservations
