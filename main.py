from jp_tokenizer.utils import read_words_from_csv
from jp_tokenizer.core import get_i_adjectives, get_na_adjectives, get_verbs


if __name__ == '__main__':
    words = list()
    content = read_words_from_csv('data/vocabulary_65001.csv')
    for line in content:
        words.append(line[0])

    adj_list = get_i_adjectives(words)
    print(adj_list)
    print(len(adj_list))

    adj_list = get_na_adjectives(words)
    print(adj_list)
    print(len(adj_list))

    verb_list = get_verbs(words)
    print(verb_list)
    print(len(verb_list))
