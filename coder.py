import model

def eval_i(size, prob):
    i = prob * size
    if i < 1:
        return 1
    elif i > size - 1:
        return size - 1
    else:
        return round(i)

class Encoder:
    def __init__(self, space=8):
        self.space = space

        self.a = 2**(space - 2)
        self.b = 2 * self.a
        self.c = 3 * self.a
        self.n = 4 * self.a

        self.follow = 0
        self.l = 0
        self.u = self.n

        self.dec = 0
        self.enc = 0

        self.model = model.Model()

    def extend(self):
        result = []
        done = False
        while not done:
            if self.l >= self.b:
                self.l = 2 * (self.l - self.b)
                self.u = 2 * (self.u - self.b)
                self.enc += self.follow + 1
                result.append(1)
                for i in range(self.follow):
                    result.append(0)
                self.follow = 0
            elif self.u <= self.b:
                self.l *= 2
                self.u *= 2
                self.enc += self.follow + 1
                result.append(0)
                for i in range(self.follow):
                    result.append(1)
                self.follow = 0
            elif self.l >= self.a and self.u <= self.c:
                self.l = 2 * (self.l - self.a)
                self.u = 2 * (self.u - self.a)
                self.follow += 1
            else:
                done = True
        return result

    def compress(self, next):
        self.dec += 1

        prob = self.model.get_prob()
        self.model.update(next)

        i = eval_i(self.u - self.l, prob)
        
        if next == 1:
            self.l += int(i)
        else:
            self.u = self.l + int(i)
        
        res = self.extend()    
        return res
    
    def end(self):
        result = []

        state = 0
        inc = self.b

        while state < self.l or state + 2*inc >= self.u:
            if state + 2*inc < self.u:
                state += inc
                inc = int(0.5 * inc)

                self.enc += self.follow + 1
                result.append(1)
                for i in range(self.follow):
                    result.append(0)
                self.follow = 0

            else: #state + delta > self.u
                inc = int(0.5 * inc)

                self.enc += self.follow + 1
                result.append(0)
                for i in range(self.follow):
                    result.append(1)
                self.follow = 0

        return result
    
    def get_data(self):
        d = dict()
        d["log_space"] = self.space
        d["decoded_bits"] = self.dec
        d["encoded_bits"] = self.enc
        d["model_info"] = self.model.get_data()
        return d


class Decoder:
    def __init__(self, meta):
        self.space = meta["log_space"]

        self.a = 2**(self.space - 2)
        self.b = 2 * self.a
        self.c = 3 * self.a
        self.n = 4 * self.a

        self.l = 0
        self.u = self.n

        self.state = 0
        self.inc = self.n

        info = meta["model_info"]
        self.model = model.Model(
            info["base_layers"],
            info["max_nodes"],
            info["param1"],
            info["param2"],
            info["c"]
        )
    
    def extend(self):
        done = False
        while not done:
            if self.l >= self.b:
                self.l = 2 * (self.l - self.b)
                self.u = 2 * (self.u - self.b)
                self.state = 2 * (self.state - self.b)
                self.inc *= 2
            elif self.u <= self.b:
                self.l *= 2
                self.u *= 2
                self.state = 2 * self.state
                self.inc *= 2
            elif self.l >= self.a and self.u <= self.c:
                self.l = 2 * (self.l - self.a)
                self.u = 2 * (self.u - self.a)
                self.state = 2 * (self.state - self.a)
                self.inc *= 2
            else:
                done = True
        return
    
    def increase(self):
        res = []
        done = False
        while not done:
            i = eval_i(self.u - self.l, self.model.get_prob())
            if self.state >= self.l and self.state + self.inc <= self.l + i:
                self.u = self.l + i
                res.append(0)
                self.model.update(0)
                self.extend()
            elif self.state >= self.l + i and self.state + self.inc <= self.u:
                self.l = self.l + i
                res.append(1)
                self.model.update(1)
                self.extend()
            else:
                done = True
        return res
    
    def decompress(self, next):
        if next == 1:
            self.inc = int(0.5 * self.inc)
            self.state += self.inc
        else:
            self.inc = int(0.5 * self.inc)
        
        res = self.increase()
        return res