class Joke:
    def __init__(self, body, score = None, categories = []):
        self.joke = body
        self.score = score
        self.categories = categories

    def get_joke(self):
        return self.joke
    def set_joke(self, body):
        self.joke = body

    def get_score(self):
        return self.score
    def set_score(self, score):
        self.score = score

    def get_cats(self):
        return self.categories
    def set_cats(self, cats):
        self.categories = cats
