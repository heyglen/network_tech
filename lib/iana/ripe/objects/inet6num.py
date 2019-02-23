# Copyright 2019 Glen Harmon

# inet6num Object Description
# https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-2-descriptions-of-primary-objects/4-2-3-description-of-the-inet6num-object

from .rpsl import Rpsl


class INet6Num(Rpsl):

    def __init__(self):
        self.handle = None
        self.name = None
        self.description = list()
        self.country = list()
        self.geographic_location = None
        self.language = list()
        self.sponsor_organization = None
        self.assignment_size = None
        self.abuse_contact = None
        self.status = None
        self.maintainer_lower = list()
        self.maintainer_routes = list()
        self.maintainer_domains = list()
        self.maintainer_incident_response_team = list()
        self.changed = list()
        super().__init__()

    def __str__(self):
        return '{}'.format(
            self.handle,
        )

    def html(self, heading_level=1):
        return super().html(
            title='IPv6 Allocation',
            attributes=[
                (None, self.handle),
                ('Name', self.name),
                ('Description', self.description),
                ('Country', self.country),
                ('Geographic Location', self.geographic_location),
                ('Language', self.language),
                ('Sponsor Organization', self.sponsor_organization),
                ('Abuse Contact', self.abuse_contact),
                ('Status', self.status),
                # ('Maintainer Lower', self.maintainer_lower),
                # ('Maintainer Routes', self.maintainer_routes),
                # ('Maintainer Domains', self.maintainer_domains),
                # ('Maintainer Incident Response Team', self.maintainer_incident_response_team),
                ('Change', self.changed),
                ('Organisation', self.organisation),
                # ('Admin Contact', self.admin_contact),
                # ('Technical Contact', self.technical_contact),
                ('Remarks', self.remarks),
                ('Notify', self.notify),
                ('Maintained By', self.maintained_by),
                ('Modified', self.modified),
                # ('Type', self.type_),
            ]
        )
