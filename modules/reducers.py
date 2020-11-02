
import requests
from bs4 import BeautifulSoup as bs


class Reducers:
    @staticmethod
    def dictionary_com(word, user_agent):
        url = f'https://www.dictionary.com/browse/{word}?s=t'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)

        soup = bs(r.content, "html.parser")

        definition = soup.find('span', class_='e1q3nk1v4')
        meaning = ''
        example = ''

        if definition:
            definition = definition.text.split(': ')
            meaning = definition[0].strip(".,:; ")
            try:
                example = f'- {definition[1]}\n'
            except IndexError:
                pass

        return meaning, example

    @staticmethod
    def dictionary_cambridge_org(word, user_agent):
        url = f'https://dictionary.cambridge.org/dictionary/english/{word}'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)

        soup = bs(r.content, "html.parser")

        meaning = ''
        example = ''

        definition_span = soup.find('div', class_='def-block ddef_block')

        if definition_span:
            meaning_span = definition_span.find('div', class_='def ddef_d db')
            try:
                meaning = meaning_span.text.strip(".,:; ")
            except AttributeError:
                pass

            for example_span in definition_span.findAll('div', class_='examp dexamp'):
                ex_span = example_span.find('span', class_='eg deg')
                try:
                    example += f'- {ex_span.text.capitalize().strip(".,:; ")}\n'
                except AttributeError:
                    pass

        return meaning, example
