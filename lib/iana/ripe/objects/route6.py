# Copyright 2019 Glen Harmon

# route6 Object Description
# https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-2-descriptions-of-primary-objects/4-2-6-description-of-the-route6-object

from .route import Route


class Route6(Route):

    def html(self, heading_level=1):
        return super().html(
            title='IPv6 Route',
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
                ('Aggregate Boundry', self.aggregate_boundry),
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
                # ('Maintained By', self.maintained_by),
                ('Modified', self.modified),
                # ('Type', self.type_),
            ]
        )
