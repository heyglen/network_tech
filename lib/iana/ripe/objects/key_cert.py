"""
Copyright 2019 Glen Harmon

KEY-CERT Object Description
https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-3-descriptions-of-secondary-objects/4-3-3-description-of-the-key-cert-object

"""

from .rpsl import Rpsl


class KeyCert(Rpsl):

    def __init__(self):
        self.handle = None
        self.fingerprint = None
        self.method = None
        self.owner = list()
        self.certificate = list()
        super().__init__()

    def html(self, heading_level=1):
        return super().html(
            title='Certificate',
            attributes=[
                (None, self.handle),
                ('Fingerprint', self.fingerprint),
                ('Method', self.method),
                ('Owner', self.owner),
                ('Certificate', self.certificate),
                ('Organisation', self.organisation),
                # ('Admin Contact', self.admin_contact),
                # ('Technical Contact', self.technical_contact),
                ('Remarks', self.remarks),
                ('Notify', self.notify),
                # ('Maintained By', self.maintained_by),
                ('Modified', self.modified),
                # ('Type', self.type_),
            ]
        )
