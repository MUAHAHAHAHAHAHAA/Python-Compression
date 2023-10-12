from compression import compress_to, decompress_from
import file_handler as fh

if __name__ == "__main__":
    while True:
        text = input(">> ")

        if text == "end":
            break
        else:
            data = text.split(" ")
            if data[0] == "cmp":
                try:
                    compress_to(data[1], data[2])
                except:
                    print("A error occurred")
                
            elif data[0] == "dcmp":
                try:
                    meta = fh.get_meta(data[1])
                    dec_bits = meta["decoded_bits"]
                    enc_bits = meta["encoded_bits"]

                    answer = input("Warning: " + str(dec_bits // 8) + " bytes space is needed.\nProceed? (y): ")
                    if answer == "y":
                        decompress_from(data[1], data[2])
                except:
                    print("A error occurred")