class Player:
    def __init__(self, name='Guest'):
        self.name = name
        self.best_score = self.get_best_score()

    def get_best_score(self):
        try:
            return self.best_score
        except:
            if self.name == 'Guest':
                return 0
            else:
                # Need to extract from the database the top score
                return 1
