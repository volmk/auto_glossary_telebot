class View:
    @staticmethod
    def create(word, meaning, example_list, idx=0):
        pass


class ViewSimple(View):
    @staticmethod
    def create(word, meaning, example_list, idx=0):
        res = f'{idx}. {word} - '

        if meaning:
            res += f'{meaning}\n'
        else:
            res += 'notfounddddddddddddddddddddddddd\n'

        if example_list:
            for example in example_list:
                res += f'- {example}\n'

        return res


class ViewHtml(View):
    @staticmethod
    def create(word, meaning, example_list, idx=0):
        res = f'<b>{idx}. {word}</b> - '
        if meaning:
            res += f'{meaning}\n'
        else:
            res += 'notfounddddddddddddddddddddddddd\n'

        if example_list:
            for example in example_list:
                res += f'<i>- {example}\n</i>'

        return res
