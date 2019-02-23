# Copyright 2019 Glen Harmon

from .objects import INetNum, INet6Num, Route, Route6, AsBlock, Irt, KeyCert, Maintainer, Organisation, Person, Poem, PoeticForm, Role
from .exceptions import InvalidRipeType


TYPE_OBJECT_MAP = {
    'inetnum': INetNum,
    'inet6num': INet6Num,
    'route': Route,
    'route6': Route6,
    'as-block': AsBlock,
    'irt': Irt,
    'key-cert': KeyCert,
    'mntner': Maintainer,
    'organisation': Organisation,
    'person': Person,
    'poem': Poem,
    'poetic-form': PoeticForm,
    'role': Role,
}


def get_type_instance(ripe_type):
    if ripe_type not in TYPE_OBJECT_MAP:
        raise InvalidRipeType('Invalid RIPE object Type "{}"'.format(ripe_type))
    return TYPE_OBJECT_MAP[ripe_type]()
