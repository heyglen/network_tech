


class Base:
    _REGIONAL_INTERNET_REGISTERS = [
        'iana',
        'arin',
        'lacnic',
        'ripe',
        'afrinic',
        'apnic',
    ]

    def __init__(self):
        self.prefix = None
        self.status = None
        self.date = None
        self._rir = False

    def __repr__(self):
        return '<{} {}>'.format(
            self.__class__.__name__,
            self.__str__(),
        )
