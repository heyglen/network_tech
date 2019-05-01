"""
Copyright 2019 Glen Harmon

MNTNER Object Description
https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-3-descriptions-of-secondary-objects/4-3-4-description-of-the-mntner-object

"""

from .rpsl import Rpsl


class Maintainer(Rpsl):

    def __init__(self):
        self.handle = None
        self.description = list()
        self.update_to = list()
        self.maintainer_notify = list()
        self.authentication = list()
        super().__init__()

    def html(self, heading_level=1):
        return super().html(
            title='Maintainer',
            attributes=[
                (None, self.handle),
                ('Description', self.description),
                ('Update To', self.update_to),
                ('Maintainer Notify', self.maintainer_notify),
                ('Authentication', self.authentication),
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
