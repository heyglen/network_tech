# Copyright 2019 Glen Harmon

# route Object Description
# https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-2-descriptions-of-primary-objects/4-2-5-description-of-the-route-object

from .rpsl import Rpsl


class Route(Rpsl):

    def __init__(self):
        self.handle = None
        self.description = list()
        self.origin = None
        self.pingable = list()
        self.ping_handle = list()
        self.holes = list()
        self.member_of = list()
        self.inject = list()
        self.aggregate_method = None
        self.aggregation_boundry = set()
        self.export_policy_filter = None
        self.components = None
        self.maintainer_lower = list()
        self.maintainer_routes = list()
        self.changed = list()
        super().__init__()

    def __str__(self):
        return 'AS{} {}'.format(
            self.origin,
            self.handle,
        )

    def html(self, heading_level=1):
        return super().html(
            title='IPv4 Route',
            attributes=[
                (None, self.handle),
                ('Description', self.description),
                ('Origin', self.origin),
                ('Pingable', self.pingable),
                ('Ping Handle', self.ping_handle),
                ('Holes', self.holes),
                ('Member Of', self.member_of),
                ('Inject', self.inject),
                ('Aggregate Method', self.aggregate_method),
                ('Aggregate Boundry', self.aggregation_boundry),
                ('Export Policy Filter', self.export_policy_filter),
                ('Components', self.components),
                # ('Maintainer Lower', self.maintainer_lower),
                # ('Maintainer Routes', self.maintainer_routes),
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
