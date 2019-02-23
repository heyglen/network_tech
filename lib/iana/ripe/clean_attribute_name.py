# Copyright 2019 Glen Harmon

BASE_OBJECT_ATTRIBUTE_MAP = {
        'descr': 'description',
        'source': 'source',
        'created': 'created',
        'last-modified': 'modified',    
        'org': 'organisation',
        'admin-c': 'admin_contact',
        'tech-c': 'technical_contact',
        'mnt-by': 'maintained_by',
        'mnt-lower': 'maintainer_lower',
        'mnt-routes': 'maintainer_routes',
        'mnt-domains': 'maintainer_domains',
        'mnt-irt': 'maintainer_incident_response_team',
        'sponsoring-org': 'sponsor_organisation',
}


OBJECT_ATTRIBUTE_MAP = {
    'inetnum': {
        'inetnum': 'handle',
        'netname': 'name',
        'geoloc': 'geographic_location',
        'tech-c': 'technical_contact',
        'abuse-c': 'abuse_contact',
    },
    'inet6num': {
        'inet6num': 'handle',
        'netname': 'name',
        'geoloc': 'geographic_location',
        'admin-c': 'admin_contact',
        'tech-c': 'technical_contact',
        'abuse-c': 'abuse_contact',
        'assignment-size': 'assignment_size',
    },
    'route': {
        'route': 'handle',
        'ping-hdl': 'ping_handler',
        'member-of': 'member_of',
        'aggr-mtd': 'aggregate_method',
        'aggr-bndry': 'aggregation_boundry',
        'export-comps': 'export_policy_filter',
    },
    'route6': {
        'route6': 'handle',
        'ping-hdl': 'ping_handler',
        'member-of': 'member_of',
        'aggr-mtd': 'aggregate_method',
        'aggr-bndry': 'aggregation_boundry',
        'export-comps': 'export_policy_filter',
    },
    'as-block': {
        'as-block': 'handle',
    },
    'irt': {
        'irt': 'handle',
        'fax-no': 'fax',
        'e-mail': 'e_mail',
        'auth': 'authentication',
        'irt-nfy': 'irt_notify',
    },
    'key-cert': {
        'key-cert': 'handle',
        'fingerpr': 'fingerprint',
        'certif': 'certificate',
    },
    'mntner': {
        'mntner': 'handle',
        'upd-to': 'update_to',
        'mnt-nfy': 'maintainer_notify',
        'auth': 'authentication',
    },
    'organisation': {
        'organisation': 'handle',
        'org-name': 'name',
        'org-type': 'type_',
        'fax-no': 'fax',
        'e-mail': 'e_mail',
        'geoloc': 'geographic_location',
        'abuse-c': 'abuse_contact',
        'ref-nfy': 'reference_notify',
        'mnt-ref': 'maintainer_reference',
        'abuse-mailbox': 'abuse_mailbox',
    },
    'person': {
        'person': 'handle',
        'fax-no': 'fax',
        'e-mail': 'e_mail',
        'nic-hdl': 'person_id',
    },
    'poem': {
        'poem': 'handle',
    },
    'poetic-form': {
        'poetic-form': 'handle',
    },
    'role': {
        'role': 'handle',
        'fax-no': 'fax',
        'e-mail': 'e_mail',
        'nic-hdl': 'role_id',
        'abuse-mailbox': 'abuse_mailbox',
    },
}

for _, value in OBJECT_ATTRIBUTE_MAP.items():
    value.update(BASE_OBJECT_ATTRIBUTE_MAP)


def clean_attribute_name(ripe_type, name):
    value = OBJECT_ATTRIBUTE_MAP[ripe_type].get(name, name)
    if not value:
        raise ValueError('Attribute name clean failed {} "{}" -> "{}"'.format(ripe_type, name, value))
    return value