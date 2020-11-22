from fake_useragent import UserAgent


class Glossary:
    def __init__(self, reducer):
        self.ua = UserAgent()
        self.reducer = reducer

    def create(self, word, idx=0):
        meaning, example = self.reducer(word, self.ua.ie)
        res = f'{idx}. {word} - '

        if meaning:
            res += f'{meaning}\n'
        else:
            res += 'notfounddddddddddddddddddddddddd\n'

        if example:
            res += f'{example}'

        return res

    def create_html(self, word, idx=0):
        meaning, example = self.reducer(word, self.ua.ie)
        res = f'<b>{idx}. {word}</b> - '
        if meaning:
            res += f'{meaning}\n'
        else:
            res += 'notfounddddddddddddddddddddddddd\n'

        if example:
            res += f'<i>{example}</i>'

        return res

    def test(self, word):
        return self.reducer(word)

