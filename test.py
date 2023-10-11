import random

import file_handler as fh
from compression import compress_to, decompress_from
from constants import SEPARATOR, U, W

def generate(size, p, path):
    writer = fh.Writer(path)
    for i in range(size):
        if random.random() <= p:
            writer.write(U)
        else:
            writer.write(W)
    writer.end()

def repeat(text, n, path):
    writer = fh.Writer(path)
    for i in range(n):
        writer.write(text)
    writer.end()

def test(times, m_size, m_prob, read_path, path, write_path):
    good = True
    for i in range(times):
        size = int(random.random() * m_size)
        p = random.random() * m_prob
        generate(size, p, read_path)

        compress_to(read_path, path)
        decompress_from(path, write_path)

        original = fh.read(read_path)
        other = fh.read(write_path)

        if original != other:
            print(SEPARATOR)
            print(original)
            print(SEPARATOR)
            print(other)
            good = False
    
    print(SEPARATOR)
    if good:
        print("Everything is fine !!!")
    else:
        print("A error occurred !!!")

if __name__ == "__main__":
    res_path = "./test/"

    read_path = res_path + "test.txt"
    path = res_path + "compressed"
    write_path = res_path + "test_dec.txt"

    test(100, 1000, 0.2, read_path, path, write_path)