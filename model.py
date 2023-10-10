from markov import MarkovModel

class Model:
    def __init__(self, base_layers=8, max_nodes=30000, param1=3, param2=3, c=1):
        self.markov = MarkovModel(base_layers, max_nodes, param1, param2, c)

    def update(self, next):
        self.markov.update(next)

    def get_prob(self):
        return self.markov.predict()
    
    def get_data(self):
        return self.markov.get_data()