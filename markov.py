
class MarkovModel:
    def __init__(self, base_layers, max_nodes, param1, param2, c):
        self.base_layers = base_layers
        self.max_nodes = max_nodes
        self.param1 = param1
        self.param2 = param2
        self.c = c
        self.d = 2 * c

        self.state = 0

        # every node of the markov model has four entrys:
        # how often 0 was next
        # total count of going threw this node
        # address of the node to go to when 0
        # address of the node to go to when 1
        self.model = self.initial_model(self.base_layers)
    
    def initial_model(self, n):
        model = []
        for i in range(n-1):
            for j in range(2**i):
                model.append([0, 0, 2*(2**i + j) - 1, 2*(2**i + j)])
        for j in range(2**(n-1)):
            model.append([0, 0, 0, 0])
        return model
    
    def reset(self):
        self.state = 0
        self.model = self.initial_model(self.base_layers)

    def update(self, symbol):
        if len(self.model) > self.max_nodes:
            self.reset()

        node = self.model[self.state]
        node[1] += 1

        transitions = 0
        if symbol:
            transitions = node[1] - node[0]
        else:
            node[0] += 1
            transitions = node[0]

        self.state = node[symbol + 2]
        next = self.model[self.state]

        # node cloning
        if transitions >= self.param1 and next[1] - transitions >= self.param2:
            node[symbol + 2] = len(self.model)

            ratio = transitions / next[1]
            new = [0, 0, 0, 0]

            for i in range(2):
                new[i + 2] = next[i + 2]
                new[i] = ratio * next[i]
                next[i] -= new[i]

            self.state = len(self.model)
            self.model.append(new)

    def predict(self):
        node = self.model[self.state]
        return (node[0] + self.c) / (node[1] + self.d)

    def get_data(self):
        return {
            "base_layers": self.base_layers,
            "max_nodes": self.max_nodes,
            "param1": self.param1,
            "param2": self.param2,
            "c": self.c
        }

if __name__ == "__main__":
    model = MarkovModel(1, 10000, 2, 2, 1)
    print(model)