"""
Copyright 2019 Glen Harmon

Role Object Description
https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-3-descriptions-of-secondary-objects/4-3-9-description-of-the-role-object

"""

from .rpsl import Rpsl


class Role(Rpsl):

    def __init__(self):
        self.handle = None
        self.address = list()
        self.phone = list()
        self.fax = list()
        self.e_mail = list()

        self.reference_notify = None
        self.maintainer_reference = None
        self.abuse_mailbox = list()
        self.role_id = None
        super().__init__()

    def html(self, heading_level=1):
        return super().html(
            title='Role',
            attributes=[
                (None, self.handle),
                ('Address', self.address),
                ('Phone', self.phone),
                ('Fax', self.fax),
                ('E-Mail', self.e_mail),
                ('Reference Notify', self.reference_notify),
                ('Maintainer Reference', self.maintainer_reference),
                ('Abuse Mailbox', self.abuse_mailbox),
                ('Organisation', self.organisation),
                ('Admin Contact', self.admin_contact),
                ('Technical Contact', self.technical_contact),
                ('Remarks', self.remarks),
                ('Notify', self.notify),
                ('Maintained By', self.maintained_by),
                ('Modified', self.modified),
                ('Type', self.type_),
            ]
        )
