import re
import ipaddress
import logging

import sublime
import sublime_plugin

logger = logging.getLogger('net_tech')
logger.handlers = []
logger.setLevel(logging.DEBUG)


class DotDict(dict):
    """dot.notation access to dictionary attributes"""
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(*args):
        val = dict.get(*args)
        return DotDict(val) if type(val) is dict else val

SYNTAX = DotDict({
    'asa': 'Packages/network_tech/cisco-asa.sublime-syntax',
    'ace': 'Packages/network_tech/cisco-ace.sublime-syntax',
    'ios': 'Packages/network_tech/cisco-ios.sublime-syntax',
    'nxos': 'Packages/network_tech/cisco-nxos.sublime-syntax',
})

detect_syntax = DotDict({
    'cisco': [
        '^Current configuration : \d+ bytes$',
        '^Building configuration...\s*$',
        '^! Last configuration change at',
    ],
    'asa': [
        '^ASA Version \d+\.\d+\(\d+\)$',
    ],
    'nxos': [
        '^!Command: show ',
    ],
    'ace': [
        '^Generating configuration....',
    ],
    'ios': [
        '^Current configuration : \d+ bytes$',
        '^Building configuration...\s*$',
    ],
})

ip = DotDict({
    'v4': {
        'host': re.compile(r"""
                    (?xi)
                    (?:
                        (?!
                            (?:128\.0\.0\.0)|
                            (?:192\.0\.0\.0)|
                            (?:224\.0\.0\.0)|
                            (?:240\.0\.0\.0)|
                            (?:248\.0\.0\.0)|
                            (?:252\.0\.0\.0)|
                            (?:254\.0\.0\.0)|
                            (?:255\.0\.0\.0)|
                            (?:255\.128\.0\.0)|
                            (?:255\.192\.0\.0)|
                            (?:255\.224\.0\.0)|
                            (?:255\.240\.0\.0)|
                            (?:255\.248\.0\.0)|
                            (?:255\.252\.0\.0)|
                            (?:255\.254\.0\.0)|
                            (?:255\.255\.0\.0)|
                            (?:255\.255\.128\.0)|
                            (?:255\.255\.192\.0)|
                            (?:255\.255\.224\.0)|
                            (?:255\.255\.240\.0)|
                            (?:255\.255\.248\.0)|
                            (?:255\.255\.252\.0)|
                            (?:255\.255\.254\.0)|
                            (?:255\.255\.255\.0)|
                            (?:255\.255\.255\.128)|
                            (?:255\.255\.255\.192)|
                            (?:255\.255\.255\.224)|
                            (?:255\.255\.255\.240)|
                            (?:255\.255\.255\.248)|
                            (?:255\.255\.255\.252)|
                            (?:255\.255\.255\.254)|
                            (?:255\.255\.255\.255)|
                            (?:127\.255\.255\.255)|
                            (?:63\.255\.255\.255)|
                            (?:31\.255\.255\.255)|
                            (?:15\.255\.255\.255)|
                            (?:7\.255\.255\.255)|
                            (?:3\.255\.255\.255)|
                            (?:1\.255\.255\.255)|
                            (?:0\.255\.255\.255)|
                            (?:0\.127\.255\.255)|
                            (?:0\.63\.255\.255)|
                            (?:0\.31\.255\.255)|
                            (?:0\.15\.255\.255)|
                            (?:0\.7\.255\.255)|
                            (?:0\.3\.255\.255)|
                            (?:0\.1\.255\.255)|
                            (?:0\.0\.255\.255)|
                            (?:0\.0\.127\.255)|
                            (?:0\.0\.63\.255)|
                            (?:0\.0\.31\.255)|
                            (?:0\.0\.15\.255)|
                            (?:0\.0\.7\.255)|
                            (?:0\.0\.3\.255)|
                            (?:0\.0\.1\.255)|
                            (?:0\.0\.0\.255)|
                            (?:0\.0\.0\.127)|
                            (?:0\.0\.0\.63)|
                            (?:0\.0\.0\.31)|
                            (?:0\.0\.0\.15)|
                            (?:0\.0\.0\.7)|
                            (?:0\.0\.0\.3)|
                            (?:0\.0\.0\.1)|
                            (?:0\.0\.0\.0)
                        )
                        (?:(?:[1-2]?\d{1,2}\.){3}[1-2]?\d{1,2})
                    )
        """),
        'any': re.compile(
            r"""
            (?xi)
            (?:
                (?:
                    (?:
                        (?:
                            (?:host)|
                            (?:range)
                        )
                        \s+
                    )?
                    (?P<ip>
                        (?:
                            (?!
                                (?:128\.0\.0\.0)|
                                (?:192\.0\.0\.0)|
                                (?:224\.0\.0\.0)|
                                (?:240\.0\.0\.0)|
                                (?:248\.0\.0\.0)|
                                (?:252\.0\.0\.0)|
                                (?:254\.0\.0\.0)|
                                (?:255\.0\.0\.0)|
                                (?:255\.128\.0\.0)|
                                (?:255\.192\.0\.0)|
                                (?:255\.224\.0\.0)|
                                (?:255\.240\.0\.0)|
                                (?:255\.248\.0\.0)|
                                (?:255\.252\.0\.0)|
                                (?:255\.254\.0\.0)|
                                (?:255\.255\.0\.0)|
                                (?:255\.255\.128\.0)|
                                (?:255\.255\.192\.0)|
                                (?:255\.255\.224\.0)|
                                (?:255\.255\.240\.0)|
                                (?:255\.255\.248\.0)|
                                (?:255\.255\.252\.0)|
                                (?:255\.255\.254\.0)|
                                (?:255\.255\.255\.0)|
                                (?:255\.255\.255\.128)|
                                (?:255\.255\.255\.192)|
                                (?:255\.255\.255\.224)|
                                (?:255\.255\.255\.240)|
                                (?:255\.255\.255\.248)|
                                (?:255\.255\.255\.252)|
                                (?:255\.255\.255\.254)|
                                (?:255\.255\.255\.255)|
                                (?:127\.255\.255\.255)|
                                (?:63\.255\.255\.255)|
                                (?:31\.255\.255\.255)|
                                (?:15\.255\.255\.255)|
                                (?:7\.255\.255\.255)|
                                (?:3\.255\.255\.255)|
                                (?:1\.255\.255\.255)|
                                (?:0\.255\.255\.255)|
                                (?:0\.127\.255\.255)|
                                (?:0\.63\.255\.255)|
                                (?:0\.31\.255\.255)|
                                (?:0\.15\.255\.255)|
                                (?:0\.7\.255\.255)|
                                (?:0\.3\.255\.255)|
                                (?:0\.1\.255\.255)|
                                (?:0\.0\.255\.255)|
                                (?:0\.0\.127\.255)|
                                (?:0\.0\.63\.255)|
                                (?:0\.0\.31\.255)|
                                (?:0\.0\.15\.255)|
                                (?:0\.0\.7\.255)|
                                (?:0\.0\.3\.255)|
                                (?:0\.0\.1\.255)|
                                (?:0\.0\.0\.255)|
                                (?:0\.0\.0\.127)|
                                (?:0\.0\.0\.63)|
                                (?:0\.0\.0\.31)|
                                (?:0\.0\.0\.15)|
                                (?:0\.0\.0\.7)|
                                (?:0\.0\.0\.3)|
                                (?:0\.0\.0\.1)|
                                (?:0\.0\.0\.0)
                            )
                            (?:(?:\d{1,3}\.){3}\d{1,3})
                        )|
                        (?:(?:(?:(?:[0-9a-f]{1,4}:){7}(?:[0-9a-f]{1,4}|:))|(?:(?:[0-9a-f]{1,4}:){6}(?::[0-9a-f]{1,4}|(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3})|:))|(?:(?:[0-9a-f]{1,4}:){5}(?:(?:(?::[0-9a-f]{1,4}){1,2})|:(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3})|:))|(?:(?:[0-9a-f]{1,4}:){4}(?:(?:(?::[0-9a-f]{1,4}){1,3})|(?:(?::[0-9a-f]{1,4})?:(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(?:(?:[0-9a-f]{1,4}:){3}(?:(?:(?::[0-9a-f]{1,4}){1,4})|(?:(?::[0-9a-f]{1,4}){0,2}:(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(?:(?:[0-9a-f]{1,4}:){2}(?:(?:(?::[0-9a-f]{1,4}){1,5})|(?:(?::[0-9a-f]{1,4}){0,3}:(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(?:(?:[0-9a-f]{1,4}:){1}(?:(?:(?::[0-9a-f]{1,4}){1,6})|(?:(?::[0-9a-f]{1,4}){0,4}:(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(?::(?:(?:(?::[0-9a-f]{1,4}){1,7})|(?:(?::[0-9a-f]{1,4}){0,5}:(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:)))(?:%.+)?)
                    )
                )
                (?:
                    (?:
                        /
                        (?P<prefix_length>
                            \d{1,3}
                        )
                    )|
                    (?:
                        \s+
                        (?:
                            (?:mask\s+)?
                            (?:
                                (?P<netmask>
                                    (?:
                                        (?:0\.0\.0\.0)|
                                        (?:128\.0\.0\.0)|
                                        (?:192\.0\.0\.0)|
                                        (?:224\.0\.0\.0)|
                                        (?:240\.0\.0\.0)|
                                        (?:248\.0\.0\.0)|
                                        (?:252\.0\.0\.0)|
                                        (?:254\.0\.0\.0)|
                                        (?:255\.0\.0\.0)|
                                        (?:255\.128\.0\.0)|
                                        (?:255\.192\.0\.0)|
                                        (?:255\.224\.0\.0)|
                                        (?:255\.240\.0\.0)|
                                        (?:255\.248\.0\.0)|
                                        (?:255\.252\.0\.0)|
                                        (?:255\.254\.0\.0)|
                                        (?:255\.255\.0\.0)|
                                        (?:255\.255\.128\.0)|
                                        (?:255\.255\.192\.0)|
                                        (?:255\.255\.224\.0)|
                                        (?:255\.255\.240\.0)|
                                        (?:255\.255\.248\.0)|
                                        (?:255\.255\.252\.0)|
                                        (?:255\.255\.254\.0)|
                                        (?:255\.255\.255\.0)|
                                        (?:255\.255\.255\.128)|
                                        (?:255\.255\.255\.192)|
                                        (?:255\.255\.255\.224)|
                                        (?:255\.255\.255\.240)|
                                        (?:255\.255\.255\.248)|
                                        (?:255\.255\.255\.252)|
                                        (?:255\.255\.255\.254)|
                                        (?:255\.255\.255\.255)
                                    )
                                )|
                                (?P<wildcard>
                                    (?:
                                      (?:127\.255\.255\.255)|
                                      (?:63\.255\.255\.255)|
                                      (?:31\.255\.255\.255)|
                                      (?:15\.255\.255\.255)|
                                      (?:7\.255\.255\.255)|
                                      (?:3\.255\.255\.255)|
                                      (?:1\.255\.255\.255)|
                                      (?:0\.255\.255\.255)|
                                      (?:0\.127\.255\.255)|
                                      (?:0\.63\.255\.255)|
                                      (?:0\.31\.255\.255)|
                                      (?:0\.15\.255\.255)|
                                      (?:0\.7\.255\.255)|
                                      (?:0\.3\.255\.255)|
                                      (?:0\.1\.255\.255)|
                                      (?:0\.0\.255\.255)|
                                      (?:0\.0\.127\.255)|
                                      (?:0\.0\.63\.255)|
                                      (?:0\.0\.31\.255)|
                                      (?:0\.0\.15\.255)|
                                      (?:0\.0\.7\.255)|
                                      (?:0\.0\.3\.255)|
                                      (?:0\.0\.1\.255)|
                                      (?:0\.0\.0\.255)|
                                      (?:0\.0\.0\.127)|
                                      (?:0\.0\.0\.63)|
                                      (?:0\.0\.0\.31)|
                                      (?:0\.0\.0\.15)|
                                      (?:0\.0\.0\.7)|
                                      (?:0\.0\.0\.3)|
                                      (?:0\.0\.0\.1)|
                                      (?:0\.0\.0\.0)
                                    )
                                )
                            )
                        )
                    )
                )?
            )
            """
        ),
        'network':  re.compile(
                    r"""
                    (?xi)
                    (?:
                        (?P<ip>
                            (?:
                                (?!
                                    (?:128\.0\.0\.0)|
                                    (?:192\.0\.0\.0)|
                                    (?:224\.0\.0\.0)|
                                    (?:240\.0\.0\.0)|
                                    (?:248\.0\.0\.0)|
                                    (?:252\.0\.0\.0)|
                                    (?:254\.0\.0\.0)|
                                    (?:255\.0\.0\.0)|
                                    (?:255\.128\.0\.0)|
                                    (?:255\.192\.0\.0)|
                                    (?:255\.224\.0\.0)|
                                    (?:255\.240\.0\.0)|
                                    (?:255\.248\.0\.0)|
                                    (?:255\.252\.0\.0)|
                                    (?:255\.254\.0\.0)|
                                    (?:255\.255\.0\.0)|
                                    (?:255\.255\.128\.0)|
                                    (?:255\.255\.192\.0)|
                                    (?:255\.255\.224\.0)|
                                    (?:255\.255\.240\.0)|
                                    (?:255\.255\.248\.0)|
                                    (?:255\.255\.252\.0)|
                                    (?:255\.255\.254\.0)|
                                    (?:255\.255\.255\.0)|
                                    (?:255\.255\.255\.128)|
                                    (?:255\.255\.255\.192)|
                                    (?:255\.255\.255\.224)|
                                    (?:255\.255\.255\.240)|
                                    (?:255\.255\.255\.248)|
                                    (?:255\.255\.255\.252)|
                                    (?:255\.255\.255\.254)|
                                    (?:255\.255\.255\.255)|
                                    (?:127\.255\.255\.255)|
                                    (?:63\.255\.255\.255)|
                                    (?:31\.255\.255\.255)|
                                    (?:15\.255\.255\.255)|
                                    (?:7\.255\.255\.255)|
                                    (?:3\.255\.255\.255)|
                                    (?:1\.255\.255\.255)|
                                    (?:0\.255\.255\.255)|
                                    (?:0\.127\.255\.255)|
                                    (?:0\.63\.255\.255)|
                                    (?:0\.31\.255\.255)|
                                    (?:0\.15\.255\.255)|
                                    (?:0\.7\.255\.255)|
                                    (?:0\.3\.255\.255)|
                                    (?:0\.1\.255\.255)|
                                    (?:0\.0\.255\.255)|
                                    (?:0\.0\.127\.255)|
                                    (?:0\.0\.63\.255)|
                                    (?:0\.0\.31\.255)|
                                    (?:0\.0\.15\.255)|
                                    (?:0\.0\.7\.255)|
                                    (?:0\.0\.3\.255)|
                                    (?:0\.0\.1\.255)|
                                    (?:0\.0\.0\.255)|
                                    (?:0\.0\.0\.127)|
                                    (?:0\.0\.0\.63)|
                                    (?:0\.0\.0\.31)|
                                    (?:0\.0\.0\.15)|
                                    (?:0\.0\.0\.7)|
                                    (?:0\.0\.0\.3)|
                                    (?:0\.0\.0\.1)|
                                    (?:0\.0\.0\.0)
                                )
                                (?:(?:\d{1,3}\.){3}\d{1,3})
                            )|
                            (?:(?:(?:(?:[0-9a-f]{1,4}:){7}(?:[0-9a-f]{1,4}|:))|(?:(?:[0-9a-f]{1,4}:){6}(?::[0-9a-f]{1,4}|(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3})|:))|(?:(?:[0-9a-f]{1,4}:){5}(?:(?:(?::[0-9a-f]{1,4}){1,2})|:(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3})|:))|(?:(?:[0-9a-f]{1,4}:){4}(?:(?:(?::[0-9a-f]{1,4}){1,3})|(?:(?::[0-9a-f]{1,4})?:(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(?:(?:[0-9a-f]{1,4}:){3}(?:(?:(?::[0-9a-f]{1,4}){1,4})|(?:(?::[0-9a-f]{1,4}){0,2}:(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(?:(?:[0-9a-f]{1,4}:){2}(?:(?:(?::[0-9a-f]{1,4}){1,5})|(?:(?::[0-9a-f]{1,4}){0,3}:(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(?:(?:[0-9a-f]{1,4}:){1}(?:(?:(?::[0-9a-f]{1,4}){1,6})|(?:(?::[0-9a-f]{1,4}){0,4}:(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:))|(?::(?:(?:(?::[0-9a-f]{1,4}){1,7})|(?:(?::[0-9a-f]{1,4}){0,5}:(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])){3}))|:)))(?:%.+)?)
                        )
                        (?:
                            (?:
                                /
                                (?P<prefix_length>
                                    \d{1,3}
                                )
                            )|
                            (?:
                                \s+
                                (?:
                                    (?:mask\s+)?
                                    (?:
                                        (?P<netmask>
                                            (?:
                                                (?:0\.0\.0\.0)|
                                                (?:128\.0\.0\.0)|
                                                (?:192\.0\.0\.0)|
                                                (?:224\.0\.0\.0)|
                                                (?:240\.0\.0\.0)|
                                                (?:248\.0\.0\.0)|
                                                (?:252\.0\.0\.0)|
                                                (?:254\.0\.0\.0)|
                                                (?:255\.0\.0\.0)|
                                                (?:255\.128\.0\.0)|
                                                (?:255\.192\.0\.0)|
                                                (?:255\.224\.0\.0)|
                                                (?:255\.240\.0\.0)|
                                                (?:255\.248\.0\.0)|
                                                (?:255\.252\.0\.0)|
                                                (?:255\.254\.0\.0)|
                                                (?:255\.255\.0\.0)|
                                                (?:255\.255\.128\.0)|
                                                (?:255\.255\.192\.0)|
                                                (?:255\.255\.224\.0)|
                                                (?:255\.255\.240\.0)|
                                                (?:255\.255\.248\.0)|
                                                (?:255\.255\.252\.0)|
                                                (?:255\.255\.254\.0)|
                                                (?:255\.255\.255\.0)|
                                                (?:255\.255\.255\.128)|
                                                (?:255\.255\.255\.192)|
                                                (?:255\.255\.255\.224)|
                                                (?:255\.255\.255\.240)|
                                                (?:255\.255\.255\.248)|
                                                (?:255\.255\.255\.252)|
                                                (?:255\.255\.255\.254)|
                                                (?:255\.255\.255\.255)
                                            )
                                        )|
                                        (?P<wildcard>
                                            (?:
                                              (?:127\.255\.255\.255)|
                                              (?:63\.255\.255\.255)|
                                              (?:31\.255\.255\.255)|
                                              (?:15\.255\.255\.255)|
                                              (?:7\.255\.255\.255)|
                                              (?:3\.255\.255\.255)|
                                              (?:1\.255\.255\.255)|
                                              (?:0\.255\.255\.255)|
                                              (?:0\.127\.255\.255)|
                                              (?:0\.63\.255\.255)|
                                              (?:0\.31\.255\.255)|
                                              (?:0\.15\.255\.255)|
                                              (?:0\.7\.255\.255)|
                                              (?:0\.3\.255\.255)|
                                              (?:0\.1\.255\.255)|
                                              (?:0\.0\.255\.255)|
                                              (?:0\.0\.127\.255)|
                                              (?:0\.0\.63\.255)|
                                              (?:0\.0\.31\.255)|
                                              (?:0\.0\.15\.255)|
                                              (?:0\.0\.7\.255)|
                                              (?:0\.0\.3\.255)|
                                              (?:0\.0\.1\.255)|
                                              (?:0\.0\.0\.255)|
                                              (?:0\.0\.0\.127)|
                                              (?:0\.0\.0\.63)|
                                              (?:0\.0\.0\.31)|
                                              (?:0\.0\.0\.15)|
                                              (?:0\.0\.0\.7)|
                                              (?:0\.0\.0\.3)|
                                              (?:0\.0\.0\.1)|
                                              (?:0\.0\.0\.0)
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                    """
        ),
    }
})

sublime_ip = DotDict()

sublime_re_pattern_sub = re.compile(r'P<[^>]+>')
CompiledReType = type(sublime_re_pattern_sub)


def _clean_regexp(item):
    result = None
    if isinstance(item, dict):
        result = DotDict()
        for key, value in item.items():
            result[key] = _clean_regexp(value)
    elif isinstance(item, CompiledReType):
        pattern = item.pattern
        pattern = pattern.replace(' ', '').replace('\r', '').replace('\n', '')
        result = sublime_re_pattern_sub.sub(':', pattern)
    else:
        raise TypeError('{}'.format(type(item)))
    return result

sublime_ip = _clean_regexp(ip)


class SearchHistory(list):
    @property
    def last(self):
        last = None
        if self:
            last = self[0]
        return last


class Html:

    @classmethod
    def unordered_list(cls, items):
        return cls._tag(
            'ul',
            content=[cls.li(i) for i in items],
            style='list-style-type:none'
        )

    @classmethod
    def _tag(cls, tag, content=None, style=None):
        style = ' style="{}"'.format(style or '')
        if isinstance(content, list):
            content = ''.join(content)
        content = str(content or '')
        return '<{}{}>{}</{}>'.format(tag, style, content, tag)

for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'hr', 'div', 'span', 'li']:
    setattr(
        Html,
        tag,
        classmethod(lambda cls, text='': cls._tag(tag, content=text))
    )


class SelectionUtility:

    @classmethod
    def _get_word_on_cursor(cls, view, point):
        if isinstance(point, sublime.Region):
            point = point.end()
        return view.word(point)

    @classmethod
    def _get_line_on_cursor(cls, view, point):
        if isinstance(point, sublime.Region):
            point = point.end()
        return view.line(point)

    @classmethod
    def left_word(cls, view, region, repeat=1):
        return cls._expand_words(
            view,
            region,
            classes=sublime.CLASS_WORD_END,
            repeat=repeat,
            forward=False,
        )

    @classmethod
    def right_word(cls, view, region, repeat=1):
        return cls._expand_words(
            view,
            region,
            classes=sublime.CLASS_WORD_START,
            repeat=repeat,
            forward=True,
        )

    @classmethod
    def word(cls, view, region):
        return cls._expand_words(
            view,
            region,
            classes=sublime.CLASS_WORD_START,
            repeat=0,
            forward=True,
        )

    @classmethod
    def _expand_words(cls, view, region, classes, repeat=1, forward=True):
        word = cls._get_word_on_cursor(view, region)
        line = cls._get_line_on_cursor(view, region)
        current_word = word
        for expand in range(repeat):
            next_word_end = view.find_by_class(
                current_word.end() if forward else current_word.begin(),
                forward=forward,
                classes=classes
            )
            next_word = cls._get_word_on_cursor(view, next_word_end)
            if line == cls._get_line_on_cursor(view, next_word):
                current_word = cls._get_word_on_cursor(view, next_word_end)

        start = word.begin() if forward else current_word.begin()
        end = current_word.end() if forward else word.end()
        return sublime.Region(start, end)


class Network:
    prefix_removals = [
        'host',
        'mask',
        'range'
    ]

    @classmethod
    def info(cls, network):
        """ Returns HTML formated information about the network """
        content = ''
        neighbors = cls.get_neighbors(network)
        logger.debug('Neighbors {}'.format(len(neighbors)))
        before, _, after = cls.get_neighbors(network)
        network_address = str(network.network.network_address)
        broadcast_address = str(network.network.broadcast_address)
        if network_address != broadcast_address:
            if network.version is 4:
                content = ''.join([
                    Html.span('Network: {}'.format(network.network)),
                    Html.span('Broadcast: {}'.format(broadcast_address)),
                    Html.span('# Addresses: {}'.format(network.network.num_addresses)),
                    Html.span('Masks:'),
                    Html.unordered_list(Network.masks(network)),
                ])
            else:
                content = ''.join([
                    Html.span('Network: {}/{}'.format(network_address, network.network.prefixlen)),
                ])
            if before or after:
                content += Html.span('Neighboring Networks')
            if after:
                content += Html.span(' Next: {}'.format(after.network))
            if before:
                content += Html.span(' Previous: {}'.format(before.network))
        return content

    @classmethod
    def _neighboring_network(cls, interface, after=True):
        prefix = interface.network.prefixlen
        network = interface.network
        try:
            neighbor = network.broadcast_address + 1 if after else network.network_address - 1
        except ipaddress.AddressValueError:
            return None
        return ipaddress.ip_interface('{}/{}'.format(neighbor, prefix))

    @classmethod
    def get_neighbors(cls, networks, neighbors=1):
        if not isinstance(networks, list):
            networks = [networks]
        if len(networks) is 0:
            raise ValueError('No network defined')

        before = cls._neighboring_network(networks[0], after=False)
        after = cls._neighboring_network(networks[-1], after=True)

        networks.insert(0, before)
        networks.append(after)

        remaining_neighbors = neighbors - 1
        if remaining_neighbors > 0:
            networks = cls.get_neighbors(networks, neighbors=remaining_neighbors)
        return networks

    @classmethod
    def get_network_on_cursor(cls, region, view):
        network = None
        selection_functions = [
            lambda view, region: SelectionUtility.word(view, region),
            lambda view, region: SelectionUtility.left_word(view, region),
            lambda view, region: SelectionUtility.right_word(view, region),
            lambda view, region: SelectionUtility.left_word(view, region, repeat=2),
            lambda view, region: SelectionUtility.right_word(view, region, repeat=2),
            lambda view, region: SelectionUtility.right_word(
                view, SelectionUtility.left_word(view, region).begin(), repeat=2
            ),
        ]
        for index, selection_function in enumerate(selection_functions):
            selected = selection_function(view, region)
            network_region = view.substr(selected)
            current_network = cls.get(network_region)
            if current_network:
                logger.debug('Network {} found in cursor\'s region #{}: {}'.format(
                    current_network,
                    index,
                    network_region
                ))
                if network is None or current_network.network.prefixlen < network.network.prefixlen:
                    network = current_network
            # else:
            #     logger.debug('Network not found in cursor\'s region #{}: {}'.format(
            #             index,
            #             network_region
            #         ))
        return str(network) if network else ''

    @classmethod
    def masks(cls, interface):
        return [
            '/' + str(interface.network.prefixlen),
            str(interface.netmask),
            str(interface.hostmask),
        ]

    @classmethod
    def contains(cls, group, member):
        return int(group.network.network_address) <= int(member.network.network_address) and \
            int(group.network.broadcast_address) >= int(member.network.broadcast_address)

    @classmethod
    def clean(cls, network_text):
        for remove in cls.prefix_removals:
            network_text = network_text.replace(remove, '')
        network_text = network_text.strip()
        network_text = network_text.replace('  ', ' ')
        return network_text

    @classmethod
    def _get_from_re_match(cls, network_text):
        network = None
        match = ip.v4.any.match(network_text)
        if match:
            ip_address = match.group('ip')
            prefix_length = match.group('prefix_length')
            netmask = match.group('netmask')
            wildcard = match.group('wildcard')
            mask = prefix_length or netmask or wildcard

            try:
                if mask:
                    network = ipaddress.ip_interface('/'.join([ip_address, mask]))
                else:
                    network = ipaddress.ip_interface(ip_address)
            except ValueError:
                pass
            logger.debug('Network regexp match: "{}" from {}'.format(network, match.group()))
        return network

    @classmethod
    def get(cls, network_text):
        network_text = cls.clean(network_text)
        # network_text = '/'.join(network_text.split())
        # logger.debug('bang: {}'.format(network_text))
        network = cls._get_from_re_match(network_text)
        # try:
        #     network = ipaddress.ip_interface(network_text)
        # except ValueError:
        #     network = None
        return network

    @classmethod
    def clean_region(cls, view, region):
        text = view.substr(region)
        for remove in cls.prefix_removals:
            if text.startswith(remove):
                cleaned = text.replace(remove, '').strip()
                removed_characters = len(text) - len(cleaned)
                return sublime.Region(region.begin() + removed_characters, region.end())
        return region

    @classmethod
    def clean_regions(cls, view, regions):
        cleaned = list()
        for region in regions:
            cleaned = cls.clean_region(view, region)
        return cleaned


class FindSubnetCommand(sublime_plugin.TextCommand):

    def get_network(self, network, find_all=False):
        search_network = Network.get(network)

        current_regions = self.view.sel()

        logger.debug('Searching for network {}'.format(search_network))
        if not search_network:
            logger.debug('Invalid network {}'.format(network))
        else:
            for region in self.view.sel():
                cursor = region.end()
                searched_from_start = cursor is 0

                while True:
                    found_region = self.view.find(
                        sublime_ip.v4.any,
                        cursor,
                        sublime.IGNORECASE
                    )

                    if not found_region:
                        self.view.sel().clear()

                        if not searched_from_start:
                            self.view.sel().add(sublime.Region(0, 0))
                            searched_from_start = True
                            cursor = 0
                            continue

                        self.view.sel().add_all(current_regions)
                        break

                    cleaned_region = Network.clean_region(self.view, found_region)
                    network_re_match = self.view.substr(cleaned_region)
                    logger.debug('Network RE match {}'.format(network_re_match))
                    found_network = Network.get(network_re_match)
                    logger.debug('Network Object {} generated'.format(found_network))
                    if found_network and Network.contains(search_network, found_network):
                        self.view.sel().clear()
                        self.view.show_at_center(cleaned_region.begin())
                        logger.debug('Network found in {} {}'.format(
                            cleaned_region.begin(),
                            cleaned_region.end())
                        )
                        self.view.sel().add(sublime.Region(
                            cleaned_region.begin(),
                            cleaned_region.end()
                        ))
                        break
                    cursor = cleaned_region.end()

        self._find_input_panel(network)

    def _find_input_panel(self, network=''):
        self.view.window().show_input_panel(
            caption='Find a network',
            initial_text=network,
            on_done=self.get_network,
            on_change=None,
            on_cancel=None
        )

    def run(self, edit):
        under_cursor = Network.get_network_on_cursor(self.view.sel()[0], self.view)
        default_search = under_cursor if under_cursor else ''
        self._find_input_panel(network=default_search)


class FindAllSubnetsCommand(sublime_plugin.TextCommand):

    def get_network(self, networks, find_all=False):
        search_networks = {Network.get(n) for n in networks.split(',')}

        current_regions = self.view.sel()

        logger.debug('Searching for network(s) {}'.format(networks))
        for network in search_networks:
            if not network:
                message = 'Invalid network {}'.format(network)
                logger.debug(message)
                self.view.show_popup_menu(message)
                return
        else:
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(0, 0))

            found_regions = self.view.find_all(
                sublime_ip.v4.any,
                sublime.IGNORECASE,
            )

            matching_networks = set()
            found_networks = {self.view.substr(r) for r in found_regions}
            logger.debug('Found {} IP like objects'.format(len(found_networks)))
            for found_network in found_networks:
                if found_network in matching_networks:
                    continue
                logger.debug('Getting network "{}"'.format(found_network))

                for search_network in search_networks:
                    network_object = Network.get(found_network)
                    if network_object and Network.contains(search_network, network_object):
                        matching_networks.add(found_network)
                        break

            self.view.sel().clear()
            if matching_networks:
                moved_view = False
                for region in found_regions:
                    cleaned_region = Network.clean_region(self.view, region)
                    if self.view.substr(cleaned_region) in matching_networks:
                        self.view.sel().add(cleaned_region)
                        if not moved_view:
                            self.view.show_at_center(cleaned_region.begin())
                            moved_view = True
            else:
                logger.debug('No matches')
                self.view.sel().add_all(current_regions)
                self.view.show_at_center(current_regions[0].begin())

    def _find_input_panel(self, network=''):
        self.view.window().show_input_panel(
            caption='Find all Network(s) - comma seperated',
            initial_text=network,
            on_done=self.get_network,
            on_change=None,
            on_cancel=None
        )

    def run(self, edit):
        default_search = Network.get_network_on_cursor(self.view.sel()[0], self.view)
        default_search = default_search if ip.v4.network.search(default_search) else ''
        self._find_input_panel(network=default_search)


class AutoSyntaxDetection(sublime_plugin.ViewEventListener):
    def on_modified_async(self):
        if self.is_plain_text:
            if self.is_asa:
                self.view.set_syntax_file(SYNTAX.asa)
            if self.is_ios:
                self.view.set_syntax_file(SYNTAX.ios)
            if self.is_nxos:
                self.view.set_syntax_file(SYNTAX.nxos)

    @property
    def is_plain_text(self):
        return self.view.scope_name(0).strip() == 'text.plain'

    def is_cisco(self):
        return self._syntax_detection(
            detect_syntax.cisco,
            'Cisco detected',
            check_if_cisco=False,
            status_update=False
        )

    @property
    def is_asa(self):
        return self._syntax_detection(detect_syntax.asa, 'Cisco ASA detected')

    @property
    def is_nxos(self):
        return self._syntax_detection(detect_syntax.nxos, 'Cisco NXOS detected')

    @property
    def is_ios(self):
        return self._syntax_detection(detect_syntax.ios, 'Cisco IOS detected')

    def _syntax_detection(self, syntax_list, message, check_if_cisco=True, status_update=True):
        is_cisco = self.is_cisco if check_if_cisco else lambda: True
        if is_cisco() and syntax_list:
            for evidence in syntax_list:
                if self.view.find(evidence, 0) is not None:
                    if status_update:
                        self.view.erase_status('Network Tech')
                        self.view.set_status('Network Tech', message)
                        sublime.set_timeout(
                            (lambda: self.view.erase_status('Network Tech')),
                            3000
                        )
                    logger.debug(message)
                    return True
        return False


class NetworkAutoCompleteListener(sublime_plugin.ViewEventListener):
    # def on_query_completions(self, prefix, locations):
    def on_hover(self, point, hover_zone):
        if hover_zone == sublime.HOVER_TEXT:
            if self.view.is_popup_visible():
                self.view.hide_popup()
            self.network_info(point=point, location=point)
        else:
            self.view.hide_popup()

    def on_modified_async(self):
        self.network_info()

    def network_info(self, point=None, location=None):
        regions = self.view.sel() if point is None else [sublime.Region(point, point)]
        location = regions[0].end() if location is None else location

        for region in regions:
            if not self.view.match_selector(region.end(), 'text.network'):
                continue
            match_text = Network.get_network_on_cursor(region, self.view)
            network = Network.get(match_text)
            if network:
                content = Network.info(network)
                if content:
                    if self.view.is_popup_visible():
                        self.view.update_popup(content)
                    else:
                        self.view.show_popup(
                            content,
                            flags=sublime.COOPERATE_WITH_AUTO_COMPLETE,
                            location=location,
                        )
