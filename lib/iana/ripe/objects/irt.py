"""
Copyright 2019 Glen Harmon

IRT = Incident Response Team

IRT Object Description
https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-3-descriptions-of-secondary-objects/4-3-2-description-of-the-irt-object

"""

from .rpsl import Rpsl


class Irt(Rpsl):

    def __init__(self):
        self.handle = None
        self.address = list()
        self.phone = list()
        self.fax = list()
        self.e_mail = list()
        self.signature = list()
        self.encryption = list()
        self.authentication = list()
        self.irt_notify = list()
        self.notify = list()
        super().__init__()

    def __str__(self):
        irt_name = self.handle.replace('IRT-', '')
        return '{}'.format(
            irt_name,
        )

    def html(self, heading_level=1):
        return super().html(
            title='Incident Response Team',
            attributes=[
                (None, self.handle),
                ('Address', self.address),
                ('Phone', self.phone),
                ('Fax', self.fax),
                ('E-Mail', self.e_mail),
                ('Signature', self.signature),
                ('Encryption', self.encryption),
                ('Authentication', self.authentication),
                ('Incident Response Team Notify', self.irt_notify),
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
