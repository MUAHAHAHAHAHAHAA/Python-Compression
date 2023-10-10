from markov import MarkovModel

class Model:
    def __init__(self, param1=2, param2=2):
        self.chain = MarkovModel(param1, param2)

    def update(self, next):
        self.chain.update(next)

    def get_prob(self):
        return self.chain.predict()
    
    def get_data(self):
        return self.chain.get_data()

    # unused
    def of(data):
        first = 0
        count = 0
        for value in data:
            count += 1
            if value == "u":
                first += 1
        return Model(first, count)