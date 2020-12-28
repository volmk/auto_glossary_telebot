from modules.glossary.model import Model


class ModelGer(Model):
    @staticmethod
    def create(word, user_agent):
        meaning, example_list = ModelGer.duden_de(word, user_agent)
        return meaning, example_list

    @staticmethod
    def duden_de(word, user_agent):
        try:
            soup = Model.get_soup(f'https://www.duden.de/suchen/dudenonline/{word}', user_agent)

            first_link = soup.find('a', class_='vignette__label')
            if not first_link:
                return '', []

            href = first_link['href']
            if not href:
                return '', []

            soup = Model.get_soup(f'https://www.duden.de{href}', user_agent)

            definition_block = soup.find('div', id='bedeutung')
            if definition_block:
                meaning_block = definition_block.find('p')
            else:
                definition_block = soup.find('li', id='Bedeutung-1') or soup.find('li', id='Bedeutung-1a')
                if not definition_block:
                    return '', []
                meaning_block = definition_block.find('div', class_='enumeration__text')

            if not meaning_block:
                return '', []

            meaning = meaning_block.text.strip(".,:; ")

            example_block = definition_block.find('ul', class_='note__list')
            if not example_block:
                return meaning, []
            children = example_block.findAll('li')
            example_list = list(map(lambda x: x.text.strip(".,:; "), children))
            return meaning, example_list
        except AttributeError:
            return '', []

from fake_useragent import UserAgent

print(ModelGer.duden_de('Kältebus', UserAgent().ie))