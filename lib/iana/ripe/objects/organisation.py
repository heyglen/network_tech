"""
Copyright 2019 Glen Harmon

ORGANISATION Object Description
https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-3-descriptions-of-secondary-objects/4-3-5-description-of-the-organisation-object

"""

from .rpsl import Rpsl


class Organisation(Rpsl):

    def __init__(self):
        self.handle = None
        self.address = list()
        self.name = list()
        self.type_ = None
        self.description = list()
        self.phone = list()
        self.fax = list()
        self.e_mail = list()
        self.language = list()

        self.geographic_location = None
        self.abuse_contact = None
        self.reference_notify = None
        self.maintainer_reference = None
        self.abuse_mailbox = None
        super().__init__()

    def __str__(self):
        return '{}'.format(self.name)

    def html(self, heading_level=1):
        return super().html(
            title='Organisation',
            attributes=[
                (None, self.handle),
                ('Name', self.name),
                ('Description', self.description),
                ('Phone', self.phone),
                ('Fax', self.fax),
                ('E-Mail', self.e_mail),
                ('Language', self.language),
                ('Geographic Location', self.geographic_location),
                ('Abuse Contact', self.abuse_contact),
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
