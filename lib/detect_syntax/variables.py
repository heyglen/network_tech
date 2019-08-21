from collections import namedtuple


_SYNTAX_ATTRIBUTES = 'asa ace ios nxos ios_xr'
_DETECT_SYNTAX_ATTRIBUTES = _SYNTAX_ATTRIBUTES + ' cisco'

SYNTAX = namedtuple('Syntax', _SYNTAX_ATTRIBUTES)(
    asa='Packages/Network Tech/cisco-asa.sublime-syntax',
    ace='Packages/Network Tech/cisco-ace.sublime-syntax',
    ios='Packages/Network Tech/cisco-ios.sublime-syntax',
    nxos='Packages/Network Tech/cisco-nxos.sublime-syntax',
    ios_xr='Packages/Network Tech/cisco-ios-xr.sublime-syntax',
)


DETECT_SYNTAX = namedtuple('DetectSyntax', _DETECT_SYNTAX_ATTRIBUTES)(
    cisco=[
        r'^! Last configuration change at',
        r'^!Command: show ',
        r'^: Hardware:\s+ASA\d+',
        r'^ASA Version \d+\.\d+',
        r'^Building configuration...$',
        r'^Current configuration : \d+ bytes$',
        r'^Generating configuration....',
        r'\bios-regex\s+',
        r'^\s*\bnsf\s+cisco\s*$',
    ],
    asa=[
        r'^#\s+set\s+syntax\s*=\s*cisco-asa',
        r'^ASA Version \d+\.\d+',
        r'^: Hardware:\s+ASA\d+',
        r'^\s*security-level \d+$',
        r'^\s*nameif \S+$',
        r'^\s*access-list cached ACL log flows:',
        r'^\s*route\s+\S+\d+',
        r'^\s*fragment chain \d+ \S+$',
        r'^\s*asdm image \S+$',
        r'^\s*same-security-traffic',
    ],  
    nxos=[
        r'^#\s+set\s+syntax\s*=\s*cisco-nxos',
        r'^!Command: show .*',
        r'^\s*feature \S+',
        r'^\s*vrf context \S+',
    ],
    ace=[
        r'^#\s+set\s+syntax\s*=\s*cisco-ace',
        r'^Generating configuration....',
    ],
    ios=[
        r'^#\s+set\s+syntax\s*=\s*cisco-ios',
        r'^\s*ip classless$',
        r'^\s*!! IOS XR Configuration$',
        r'^\s*ip subnet-zero$',
        r'^\s*redundancy$',
        r'^\s*mode sso$',
        r'^\s*main-cpu$',
        r'^\s*auto-sync standard$',
        r'^\s*spanning-tree extend system-id$',
        r'^\s*vlan internal allocation policy ascending$',
        r'^Current configuration : \d+ bytes$',
        r'^Building configuration...$',
        r'^\s*access-list \d{2,3} ((?:permit)|(?:deny))',
    ],
    ios_xr=[
        r'^#\s+set\s+syntax\s*=\s*cisco-ios-xr',
        r'^\s*route-policy\s+\S+',
        r'^\s*tag-set\s+\S+\s*$',
        r'^\s*extcommunity-set\s+rt\s+\S+\s*$',
        r'^\s*extcommunity-set\s+cost\s+\S+\s*$',
        r'^\s*extcommunity-set\s+soo\s+\S+\s*$',
        r'^\s*prefix-set\s+\S+\s*$',
        r'^\s*ospf-area-set\s+\S+\s*$',
        r'^\s*as-path-set\s+\S+\s*$',
        r'^\s*rpl\s+editor\s+(?:(?:nano)|(?:emacs)|(?:vim))\s*$',
        r'^\s*rpl\s+maximum\s+(?:(?:lines)|(?:policies))\s+\d+\s*$',
    ],
)
