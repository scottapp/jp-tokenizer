

def read_words_from_csv(filename):
    with open(filename, 'r', encoding='utf8') as f:
        lines = f.readlines()
    words = list()
    for line in lines:
        cols = line.split(',')
        if cols:
            words.append(cols)
    return words
