# Copyright 2019 Glen Harmon

import functools


def rsetattr(obj, attr, value):
    attrs = attr.split('.')
    setattr(functools.reduce(getattr, attrs[:-1], obj), attrs[-1], value)
