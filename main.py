from compression import compress_to, decompress_from
import test

import file_handler as fh
import uwu

if __name__ == "__main__":
    res_path = "./resources/"

    read_path = res_path + "text.txt"
    path = res_path + "compressed"
    write_path = res_path + "text_dec.txt"

    #test.generate(100, 0.5, read_path)

    text = fh.read(res_path + "texts/article.txt")
    data = uwu.uwu(text)
    
    writer = fh.Writer(read_path)
    for string in data:
        writer.write(string)
    writer.end()
    
    compress_to(read_path, path)
    decompress_from(path, write_path)