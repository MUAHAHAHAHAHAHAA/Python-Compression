import file_handler as fh
from coder import Encoder, Decoder

def compress_to(read_path, path):
    print("-----------------")

    fh.prepare_folder(path)

    reader = fh.Reader(read_path)
    writer = fh.Writer(path + "/comp")

    comp = Encoder()

    while True:
        byte = reader.next()
        if not byte:
            break
        res = comp.compress(byte)
        for string in res:
            writer.write(string)
    
    end = comp.end()
    for string in end:
        writer.write(string)

    writer.end()

    meta = comp.get_data()

    fh.set(path + "/meta.json", meta)

    if meta["decoded_bytes"] > 0:
        ratio = round(100 * meta["encoded_bytes"] / meta["decoded_bytes"], 2)
        print("Compression: " + str(ratio) + " %")


def decompress_from(read_path, path):
    meta = fh.get(read_path + "/meta.json")
    dec_bytes = meta["decoded_bytes"]
    enc_bytes = meta["encoded_bytes"]

    print(meta)
    print("Warning: " + str(dec_bytes) + " bytes space is needed")

    comp = Decoder(meta)

    reader = fh.Reader(read_path + "/comp")
    writer = fh.Writer(path)
    
    written = 0
    next = 0

    while written < dec_bytes and next < enc_bytes:
        res = comp.decompress(reader.next())

        if written + len(res) >= dec_bytes:
            for i in range(dec_bytes - written):
                writer.write(res[i])
            break

        for byte in res:
            writer.write(byte)

        next += 1
        written += len(res)

    reader.end()
    writer.end()