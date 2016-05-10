"""
    Used to build complex regex substitutions in completions
"""


def completion_regex(match_index, options):
    expressions = list()
    completions = list()
    for word in options:
        for index, letter in enumerate(word):
            index = index + 1
            if len(word) < index:
                break
            expression = '({}$)'.format(word[:index])
            completion = word[index:]
            if not word[:index] or not word[index:]:
                continue
            expressions.append(expression)
            completions.append(completion)
    expressions.append('.*')
    expression = '|'.join(expressions)
    replace = ''
    for index, completion in enumerate(completions):
        index = index + 1
        replace = '{}?{}:{}:'.format(replace, index, completion)
    replace = replace.rstrip(':')
    expression = '${{{}/{}/{}/i}}'.format(match_index, expression, replace)
    return expression


options = [
    'host',
]

text = completion_regex(1, options)
print text
