def print_words(inputfile):
    words = []
    with open(inputfile) as f:
        for word in f.readlines():
            word_ = word.replace("\n", "").replace(" ", "").upper().lower()
            words.append("\\textsc{"+f"{word_}"+"}")
    print(", ".join(words))


if __name__ == '__main__':
    import plac
    plac.call(print_words)
