
from .base import Base


class Ipv6Record(Base):

    def __init__(self):
        self.description = None
        self.notes = None
        super().__init__()


    def __str__(self):
        return '{} {}'.format(
            self.prefix,
            self.rir,
        )

    @property
    def rir(self):
        """ Regional Internet Registry """
        if self._rir is False:
            self._rir = None
            rir = self.description.lower()
            for register in self._REGIONAL_INTERNET_REGISTERS:
                if register in rir:
                    self._rir = register.upper()
                    break
        return self._rir