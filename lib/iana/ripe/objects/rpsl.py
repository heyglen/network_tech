"""

Copyright 2019 Glen Harmon


RPSL Common Attributes
https://www.ripe.net/manage-ips-and-asns/db/support/documentation/ripe-database-documentation/rpsl-object-types/4-1-description-of-attributes-common-to-all-objects
"""

class Rpsl:

    def __init__(self):
        self.organisation = list()
        self.admin_contact = list()
        self.technical_contact = list()
        self.remarks = list()
        self.notify = list()
        self.maintained_by = list()

        self.source = None
        self.created = None
        self.modified = None
        self.type_ = None

    def __repr__(self):
        return '<{} {}>'.format(
            type(self).__name__,
            self.__str__(),
        )

    def __str__(self):
        return '{}'.format(self.handle)

    def __eq__(self, value):
        if issubclass(value.__class__, self.__class__):
            return value.__class__ is self.__class__ and value.handle == self.handle
        return False

    def __hash__(self):
        return hash((self.type_, self.handle))

    def html(self, title, attributes, heading_level=1):
        text = """
            <h{0}>{1}</h{0}>
        """.format(
            heading_level,
            title,
        )
        for label, value in attributes:
            if not value:
                continue

            if isinstance(value, (list, set)):
                if label:
                    text += """<p>
                        <div>{}: </div>
                    """.format(label)
                for entry in value:
                    text += '<div>{}</div>\n'.format(entry)
                text += '</p>\n'
            else:
                if label:
                    text += """<p>
                        <span>{}: </span><span>{}</span>
                    </p>
                    """.format(label, value)
                else:
                    text += """<p>
                        <span>{}</span>
                    </p>
                    """.format(value)
        return text