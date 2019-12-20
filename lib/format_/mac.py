
VALID_HEX_CHARACTERS = '1234567890abcdef'


def _reformat(mac, separator, digit_grouping):
    for find in (':', '.', '-'):
        mac = mac.replace(find, '')

    if len(mac) != 12:
        raise ValueError('Invalid MAC address "{}".\nMACs contain 12 digits'.format(mac))

    mac = mac.lower()
    formatted_mac = list()
    for index, digit in enumerate(mac):
        if digit not in VALID_HEX_CHARACTERS:
            raise ValueError('Invalid MAC address "{}".\nMACs contain only HEX digits'.format(mac))
        if ((index + 0) % digit_grouping) == 0:
            formatted_mac.append(separator)
        formatted_mac.append(digit)
    return ''.join(formatted_mac).strip(separator)

def colon(mac):
    """ aa:aa:aa:aa:aa:aa """
    return _reformat(mac, separator=':', digit_grouping=2)


def dash(mac):
    """ aa-aa-aa-aa-aa-aa """
    return _reformat(mac, separator='-', digit_grouping=2)


def dot(mac):
    """ aaaa.aaaa.aaaa """
    return _reformat(mac, separator='.', digit_grouping=4)
