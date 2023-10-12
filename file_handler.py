import json
import os

class Writer:
    def __init__(self, path):
        self.file = open(path, "wb")
    
    def write(self, data):
        self.file.write(data)
    
    def end(self):
        self.file.close()

class Reader:
    def __init__(self, path, offset=0):
        self.file = open(path, "rb")
        self.file.seek(offset)
    
    def next(self):
        return self.file.read(1)
    
    def end(self):
        self.file.close()

def get_meta(path):
    pos = os.path.getsize(path)
    chars = []
    file = open(path, "r")
    while True:
        file.seek(pos)
        char = file.read(1)
        if char == "\n":
            break
        chars.insert(0, char)
        pos -= 1
    return json.loads("".join(chars))

def add(path, dict):
    file = open(path, "a")
    file.write("\n" + json.dumps(dict))
    file.close()

def set(path, data):
    file = open(path, mode="w")
    file.write(json.dumps(data))
    file.close()

def get(path):
    file = open(path, mode="r")
    text = file.read()
    file.close()
    return json.loads(text)

def read(path):
    file = open(path, mode="r")
    data = file.read()
    file.close()
    return data

def write(path, data):
    file = open(path, mode="w")
    file.write(data)
    file.close()

if __name__ == "__main__":
    """
    path = "test.txt"
    data, length = get_meta(path)
    reader = Reader(path, length+1)
    while True:
        bytes = reader.next()
        if not bytes:
            break
        print(chr(bytes[0]))
    """
    text = '{"log_space": 8, "decoded_bits": 5299632, "encoded_bits": 169509, "model_info": {"base_layers": 8, "max_nodes": 30000, "param1": 3, "param2": 3, "c": 1}}'
    print(len(text))