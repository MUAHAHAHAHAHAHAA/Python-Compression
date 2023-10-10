import uwu

class MarkovModel:
    def __init__(self, param1, param2, c=1):
        self.param1 = param1
        self.param2 = param2
        self.c = c
        self.d = 2 * c

        self.state = 0

        # how often u was next
        # total count of going threw this node
        # address of the node to go to when u
        # address of the node to go to when 2
        self.model = [
            [0, 0, 0, 0]
        ]

    def update(self, symbol):
        node = self.model[self.state]
        node[1] += 1

        transitions = 0
        pos = 2
        if symbol== "u":
            self.state = node[2]
            node[0] += 1
            transitions = node[0]
        else: # symbol is "w"
            self.state = node[3]
            transitions = node[1] - node[0]
            pos = 3

        next = self.model[self.state]

        # node cloning
        if transitions >= self.param1 and next[1] - transitions >= self.param2:
            #next[0], next[1] = 0, 0
            node[pos] = len(self.model)
            new = [next[0], next[1], next[2], next[3]]
            self.model.append(new)

    def predict(self):
        node = self.model[self.state]
        return (node[0] + self.c) / (node[1] + self.d)

    def get_data(self):
        return {
            "param1": self.param1,
            "param2": self.param2,
            "c": self.c
        }

if __name__ == "__main__":
    text = 50 * "uw"

    mark = MarkovModel(2, 2)

    for char in text:
        mark.update(char)

    print("-------------")
    print(mark.model)
    print(len(mark.model))

    prob = mark.predict()
    print(prob)