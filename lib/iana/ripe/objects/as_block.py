# Copyright 2019 Glen Harmon

# AS-BLOCK Object Description
# https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-3-descriptions-of-secondary-objects/4-3-1-description-of-the-as-block-object

from .rpsl import Rpsl


class AsBlock(Rpsl):

    def __init__(self):
        self.handle = None
        self.description = list()
        self.maintainer_lower = list()
        self.maintainer_routes = list()
        self.changed = list()
        super().__init__()

    def __str__(self):
        as_number = self.handle.replace('AS', '')
        return 'AS{}'.format(
            as_number,
        )

    def html(self, heading_level=1):
        return super().html(
            title='IPv6 AS Block',
            attributes=[
                (None, self.handle),
                ('Description', self.description),
                ('Maintainer Lower', self.maintainer_lower),
                ('Maintainer Routes', self.maintainer_routes),
                ('Change', self.changed),
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
