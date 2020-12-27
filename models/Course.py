class Course:
    def __init__(self, category, name, prize, url, rank):
        self._category = category
        self._name = name
        self._prize = prize
        self._url = url
        self._rank = rank
    
    @property
    def category(self):
        return self._category
    
    @property
    def name(self):
        return self._name

    @property
    def prize(self):
        return self._prize
    
    @property
    def url(self):
        return self._url

    @property
    def rank(self):
        return self._rank   

    def __str__(self):
        return "Curso {} en categoria {} a {}".format(self.name, self.category, self.prize)