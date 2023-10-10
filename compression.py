import file_handler as fh
from coder import Encoder, Decoder
from binary import as_bits, Buffer
from constants import *

def compress_to(read_path, path):
    print(SEPARATOR)

    fh.prepare_folder(path)

    reader = fh.Reader(read_path)
    writer = fh.Writer(path + "/comp")

    b = Buffer()
    comp = Encoder()

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

    b.add(comp.end())
    res = b.finish()
    
    for byte in res:
        writer.write(byte)

    writer.end()

    meta = comp.get_data()
    #print(meta)

    fh.set(path + "/meta.json", meta)

    if meta["decoded_bits"] > 0:
        ratio = round(100 * meta["encoded_bits"] / meta["decoded_bits"], 2)
        print("Compression: " + str(ratio) + " %")


def decompress_from(read_path, path):
    meta = fh.get(read_path + "/meta.json")
    dec_bits = meta["decoded_bits"]
    enc_bits = meta["encoded_bits"]

    print("Warning: " + str(dec_bits // 8) + " bytes space is needed")

    b = Buffer()
    comp = Decoder(meta)

    reader = fh.Reader(read_path + "/comp")
    writer = fh.Writer(path)
    
    read_bits = 0
    written_bits = 0

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

    reader.end()
    writer.end()