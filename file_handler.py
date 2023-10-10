import json
import os

class Writer:
    def __init__(self, path):
        self.file = open(path, "w+")
    
    def write(self, data):
        self.file.write(data)
    
    def end(self):
        self.file.close()

class Reader:
    def __init__(self, path):
        self.file = open(path, "r")
    
    def next(self):
        return self.file.read(1)
    
    def end(self):
        self.file.close()

def read(path):
    file = open(path, mode="r")
    data = file.read()
    file.close()
    return data

def write(path, data):
    file = open(path, mode="w")
    file.write(data)
    file.close()

def set(path, data):
    file = open(path, mode="w")
    file.write(json.dumps(data))
    file.close()

def get(path):
    file = open(path, mode="r")
    data = json.load(file)
    file.close()
    return data

def prepare_folder(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        os.mkdir(path)

if __name__ == "__main__":
    path = "resources/sometext.txt"
    data = read(path)
    print(type(data))
    print(data[10])