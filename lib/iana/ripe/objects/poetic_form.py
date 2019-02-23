"""
Copyright 2019 Glen Harmon

POETIC-FORM Object Description
https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-3-descriptions-of-secondary-objects/4-3-8-description-of-the-poetic-form-object

"""

from .rpsl import Rpsl


class PoeticForm(Rpsl):

    def __init__(self):
        self.handle = None
        self.description =  list()  
        super().__init__()

    def __str__(self):
        return '{}'.format(self.handle)

    def html(self, heading_level=1):
        return super().html(
            title='Poetic Form',
            attributes=[
                (None, self.handle),
                ('Description', self.description),
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
