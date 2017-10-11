class Html:
    @classmethod
    def unordered_list(cls, items):
        return cls._tag(
            'ul',
            content=[cls.li(i) for i in items],
            style='list-style-type:none'
        )

    @classmethod
    def _tag(cls, tag, content=None, style=None):
        style = ' style="{}"'.format(style or '')
        if isinstance(content, list):
            content = ''.join(content)
        content = str(content or '')
        return '<{}{}>{}</{}>'.format(tag, style, content, tag)

for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'hr', 'div', 'span', 'li']:
    setattr(
        Html,
        tag,
        classmethod(lambda cls, text='': cls._tag(tag, content=text))
    )
