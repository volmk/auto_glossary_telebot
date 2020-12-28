import requests
from bs4 import BeautifulSoup as bs


class Model:
    @staticmethod
    def create(word, user_agent):
        pass

    @staticmethod
    def get_soup(url, user_agent):
        url = url
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)

        return bs(r.content, "html.parser")


