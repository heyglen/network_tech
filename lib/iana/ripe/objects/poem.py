"""
Copyright 2019 Glen Harmon

Poem Object Description
https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-3-descriptions-of-secondary-objects/4-3-7-description-of-the-poem-object

"""

from .rpsl import Rpsl


class Poem(Rpsl):

    def __init__(self):
        self.handle = None
        self.description =  list()  
        self.form = None
        self.text = list()
        self.author = list()
        super().__init__()

    def __str__(self):
        return '{}'.format(self.handle)

    def html(self, heading_level=1):
        return super().html(
            title='Poem',
            attributes=[
                (None, self.handle),
                ('Description', self.description),
                ('Form', self.form),
                ('Text', self.phone),
                ('Author', self.author),
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
