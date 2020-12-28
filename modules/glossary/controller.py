from fake_useragent import UserAgent


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.user_agent = UserAgent()

    def create(self, word, idx=0):
        meaning, example = self.model.create(word, self.user_agent.ie)
        return self.view.create(word, meaning, example, idx)
