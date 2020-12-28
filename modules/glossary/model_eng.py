from modules.glossary.model import Model


class ModelEng(Model):
    @staticmethod
    def create(word, user_agent):
        meaning, example_list = ModelEng.dictionary_cambridge_org(word, user_agent)
        return meaning, example_list

    @staticmethod
    def dictionary_cambridge_org(word, user_agent):
        try:
            soup = Model.get_soup(f'https://dictionary.cambridge.org/dictionary/english/{word}', user_agent)

            definition_block = soup.find('div', class_='def-block ddef_block')
            if not definition_block:
                return '', []

            meaning_block = definition_block.find('div', class_='def ddef_d db')
            if not meaning_block:
                return '', []

            meaning = meaning_block.text.strip(".,:; ")

            example_block = definition_block.findAll('div', class_='examp dexamp')
            if not example_block:
                return meaning, []

            example_list = []
            for example_span in example_block:
                ex_span = example_span.find('span', class_='eg deg')
                example_list.append(ex_span.text.strip(".,:; "))

            return meaning, example_list
        except AttributeError:
            return '', []