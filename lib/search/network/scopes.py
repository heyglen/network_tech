# Copyright 2017 Glen Harmon


from collections import namedtuple

_ipv4_scope = namedtuple('IPv4Scope', 'incomplete prefix')
_incomplete = namedtuple('IPv4Incomplete', 'ip prefix')


scopes = namedtuple('Scope', 'ipv4')(
    ipv4=_ipv4_scope(
        incomplete=_incomplete(
          ip='ip.ipv4.incomplete.ip',  
          prefix='ip.ipv4.incomplete.prefix',  
        ),
        prefix='constant.numeric.ip.ipv4.prefix',  # 1.2.3.4/24
    ),
)
