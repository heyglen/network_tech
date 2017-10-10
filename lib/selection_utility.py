import sublime


class SelectionUtility:

    @classmethod
    def _get_word_on_cursor(cls, view, point):
        if isinstance(point, sublime.Region):
            point = point.end()
        return view.word(point)

    @classmethod
    def _get_line_on_cursor(cls, view, point):
        if isinstance(point, sublime.Region):
            point = point.end()
        return view.line(point)

    @classmethod
    def left_word(cls, view, region, repeat=1):
        return cls._expand_words(
            view,
            region,
            classes=sublime.CLASS_WORD_END,
            repeat=repeat,
            forward=False,
        )

    @classmethod
    def right_word(cls, view, region, repeat=1):
        return cls._expand_words(
            view,
            region,
            classes=sublime.CLASS_WORD_START,
            repeat=repeat,
            forward=True,
        )

    @classmethod
    def word(cls, view, region):
        return cls._expand_words(
            view,
            region,
            classes=sublime.CLASS_WORD_START,
            repeat=0,
            forward=True,
        )

    @classmethod
    def _expand_words(cls, view, region, classes, repeat=1, forward=True):
        word = cls._get_word_on_cursor(view, region)
        line = cls._get_line_on_cursor(view, region)
        current_word = word
        for expand in range(repeat):
            next_word_end = view.find_by_class(
                current_word.end() if forward else current_word.begin(),
                forward=forward,
                classes=classes
            )
            next_word = cls._get_word_on_cursor(view, next_word_end)
            if line == cls._get_line_on_cursor(view, next_word):
                current_word = cls._get_word_on_cursor(view, next_word_end)

        start = word.begin() if forward else current_word.begin()
        end = current_word.end() if forward else word.end()
        return sublime.Region(start, end)
