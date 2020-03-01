import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

WORDS = 't.txt'  # words, separated with comma
GLOSS = 'gloss.txt'  # glossary


def get_span(word, user_agent):
    url = f'https://www.dictionary.com/browse/{word}?s=t'
    headers = {'User-Agent': user_agent}
    r = requests.get(url, headers=headers)

    soup = bs(r.content, "html.parser")
    all_spans = soup.findAll("span", class_="one-click-content")
    return all_spans[0].text if len(all_spans) else ''


def write_glossary(words_str):
    ua = UserAgent()

    res = ""
    for idx, s in enumerate(words_str.split(', ')):
        gloss = get_span(s.translate({' ': '%20'}), ua.ie)
        line = f'{idx + 1}. {s} – {gloss}\n'
        res += line

def get_form_file():
    with open(WORDS, 'r+') as f:
        return f.read()

def to_file(str):
    with open(GLOSS, 'w+') as f:
        f.write(str)

