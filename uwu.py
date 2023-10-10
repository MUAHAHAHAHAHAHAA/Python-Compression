
def uwu(text):
    res = []
    for char in text:
        res.append(
            '{0:08b}'.format(ord(char))
            .replace("0", "u")
            .replace("1", "w"))
    return res

if __name__ == "__main__":
    text = "Some text"
    res = uwu(text)
    print(res)