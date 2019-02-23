"""
Copyright 2019 Glen Harmon

PERSON Object Description
https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-3-descriptions-of-secondary-objects/4-3-6-description-of-the-person-object

"""

from .rpsl import Rpsl


class Person(Rpsl):

    def __init__(self):
        self.handle = None
        self.address = list()  
        self.phone = list()  
        self.fax =  list()  
        self.e_mail =  list()
        self.person_id = None
        super().__init__()

    def __str__(self):
        return '{}'.format(self.handle)

    def html(self, heading_level=1):
        return super().html(
            title='Person',
            attributes=[
                (None, self.handle),
                ('Address', self.address),
                ('Phone', self.phone),
                ('Fax', self.fax),
                ('E-Mail', self.e_mail),
                # ('Person ID', self.person_id),
                ('Organisation', self.organisation),
                ('Admin Contact', self.admin_contact),
                ('Technical Contact', self.technical_contact),
                ('Remarks', self.remarks),
                ('Notify', self.notify),
                # ('Maintained By', self.maintained_by),
                ('Modified', self.modified),
                # ('Type', self.type_),
            ]
        )
