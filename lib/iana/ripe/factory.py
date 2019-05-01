# Copyright 2019 Glen Harmon

import json

from .get_type_instance import get_type_instance
from .clean_attribute_name import clean_attribute_name
from .clean_attribute_value import clean_attribute_value


def _get_objects(response):
    body = response.json()
    return body.get('objects', dict()).get('object', list())


def _get_attributes(ripe_object):        
    attributes = ripe_object.get('attributes', dict()).get('attribute', list())
    primary_key = ripe_object.get('primary-key', dict()).get('attribute', list())
    attributes = primary_key + attributes
    return attributes

def build(response):
    objects = list()
    for ripe_object in _get_objects(response):
        type_ = ripe_object.get('type')        
        instance = get_type_instance(type_)
        instance.type_ = type_

        for attribute in _get_attributes(ripe_object):
            name = attribute['name']
            value = attribute['value']
            
            value = clean_attribute_value(type_, name, value)
            name = clean_attribute_name(type_, name)

            if not hasattr(instance, name):
                raise ValueError(
                    '{} has no attribute named "{}"\n{}'.format(
                        instance.__class__.__name__,
                        name,
                        json.dumps(ripe_object, indent=4, sort_keys=True),
                    )
                )
            attribute = getattr(instance, name)



            if isinstance(attribute, list):
                attribute.append(value)
            elif isinstance(attribute, set):
                attribute.add(value)
            else:
                setattr(instance, name, value)
    
        objects.append(instance)

    return objects


def get_sub_objects(response):

    for ripe_object in _get_objects(response):
        additional_lookups = set()

        for attribute in _get_attributes(ripe_object):
            referenced_type = attribute.get('referenced-type')
            if referenced_type:
                value = attribute['value']
                additional_lookups.add((referenced_type, value))
        return additional_lookups
