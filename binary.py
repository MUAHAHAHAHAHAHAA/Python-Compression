
def as_bits(byte):
    return [((byte >> i) & 0x01) for i in range(8)]

class Buffer:
    def __init__(self):
        self.bits = []

    def add(self, bits):
        self.bits.extend(bits)
    
    def get(self):
        res = []
        btes = len(self.bits) // 8
        for i in range(btes):
            byte = 0
            for j in range(8):
                byte = (self.bits[i * 8 + j] << j) | byte
            res.append(bytes([byte]))
        self.bits = self.bits[btes * 8:]
        return res
    
    def finish(self):
        length = len(self.bits)
        padding = (- length) % 8
        if length > 0:
            self.bits.extend([0 for i in range(padding)])
        return self.get()

if __name__ == "__main__":
    print((-5) % 8)