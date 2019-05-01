# Copyright 2017 Glen Harmon


class Html:
    @classmethod
    def unordered_list(cls, items):
        return cls._tag(
            'ul',
            text=[cls.li(i) for i in items],
            attributes={'style': 'list-style-type:none'}
        )

    @classmethod
    def _tag(cls, tag, text=None, attributes=None):
        attributes = attributes or dict()
        attributes_text = ''
        # attributes_text = ' style="{}"'.format(attributes.get('style', ''))

        for key, value in attributes.items():
            attributes_text += ' {}="{}"'.format(key, value)

        if isinstance(text, list):
            text = ''.join(text)
        text = str(text or '')
        return '<{}{}>{}</{}>'.format(tag, attributes_text, text, tag)

    @classmethod
    def h1(cls, text=None, attributes=None):
        return cls._tag('h1', text=text, attributes=attributes)

    @classmethod
    def h2(cls, text=None, attributes=None):
        return cls._tag('h2', text=text, attributes=attributes)

    @classmethod
    def h3(cls, text=None, attributes=None):
        return cls._tag('h3', text=text, attributes=attributes)

    @classmethod
    def h4(cls, text=None, attributes=None):
        return cls._tag('h4', text=text, attributes=attributes)

    @classmethod
    def h5(cls, text=None, attributes=None):
        return cls._tag('h5', text=text, attributes=attributes)

    @classmethod
    def hr(cls, text=None, attributes=None):
        return cls._tag('hr', text=text, attributes=attributes)

    @classmethod
    def div(cls, text=None, attributes=None):
        return cls._tag('div', text=text, attributes=attributes)

    @classmethod
    def span(cls, text=None, attributes=None):
        return cls._tag('span', text=text, attributes=attributes)

    @classmethod
    def li(cls, text=None, attributes=None):
        return cls._tag('li', text=text, attributes=attributes)

    @classmethod
    def img(cls, text=None, attributes=None):
        return cls._tag('img', text=text, attributes=attributes)


