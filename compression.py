import file_handler as fh
from coder import Encoder, Decoder
from binary import as_bits, Buffer
from constants import *

import os
import time

def compress_to(read_path, path):
    reader = fh.Reader(read_path)
    writer = fh.Writer(path)

    b = Buffer()
    comp = Encoder()

    t = time.time()
    read_bytes = 0
    size = os.path.getsize(read_path)

    while True:
        btes = reader.next()
        if not btes:
            break
        byte = btes[0]

        bits = as_bits(byte)
        
        for bit in bits:
            b.add(comp.compress(bit))

        res = b.get()

        for byte in res:
            writer.write(byte)
        
        read_bytes += 1
        if read_bytes == 30000//8:
            ratio = size / read_bytes - 1
            seconds = round(ratio * (time.time()-t), 2)
            t = time.time()
            print("Leftover estimation: " + str(seconds) + " seconds")
    
    seconds = round(time.time()-t, 2)
    print("Time needed: " + str(seconds) + " seconds")

    b.add(comp.end())
    res = b.finish()
    
    for byte in res:
        writer.write(byte)

    writer.end()

    meta = comp.get_data()
    #print(meta)

    #fh.set(path + "/meta.json", meta)
    fh.add(path, meta)

    if meta["decoded_bits"] > 0:
        ratio = round(100 * meta["encoded_bits"] / meta["decoded_bits"], 2)
        print("Compression: " + str(ratio) + " %")


def decompress_from(read_path, path):
    meta = fh.get_meta(read_path)
    dec_bits = meta["decoded_bits"]
    enc_bits = meta["encoded_bits"]

    b = Buffer()
    comp = Decoder(meta)

    reader = fh.Reader(read_path)
    writer = fh.Writer(path)
    
    read_bits = 0
    written_bits = 0

    t = time.time()

    while True:
        btes = reader.next()
        if not btes:
            break
        byte = btes[0]

        bits = as_bits(byte)

        if read_bits + 8 > enc_bits:
            left = enc_bits - read_bits
            for i in range(left):
                b.add(comp.decompress(bits[i]))
        else:
            for bit in bits:
                b.add(comp.decompress(bit))
        
        res = b.get()

        for byte in res:
            if written_bits < dec_bits:
                writer.write(byte)
                written_bits += 8

        read_bits += 8
        if read_bits == 30000:
            ratio = enc_bits / 30000 - 1
            seconds = round(ratio * (time.time()-t), 2)
            t = time.time()
            print("Leftover estimation: " + str(seconds) + " seconds")
    
    seconds = round(time.time()-t, 2)
    print("Time needed: " + str(seconds) + " seconds")

    reader.end()
    writer.end()