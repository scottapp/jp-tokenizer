from jp_tokenizer.utils import read_words_from_csv
from jp_tokenizer.core import get_i_adjectives, get_na_adjectives, get_verbs


if __name__ == '__main__':
    words = dict()
    content = read_words_from_csv('data/vocabulary_65001.csv')
    for line in content:
        words[line[0]] = line

    adj_list = get_i_adjectives(words)
    print(adj_list)
    print(len(adj_list))
    with open('data/all_i_adj.csv', 'w', encoding='utf8') as f:
        for word in adj_list:
            line = ','.join(words[word])
            f.write(line)

    adj_list = get_na_adjectives(words)
    print(adj_list)
    print(len(adj_list))
    with open('data/all_na_adj.csv', 'w', encoding='utf8') as f:
        for word in adj_list:
            line = ','.join(words[word])
            f.write(line)

    verb_list = get_verbs(words)
    print(verb_list)
    print(len(verb_list))
    with open('data/all_verbs.csv', 'w', encoding='utf8') as f:
        for word in verb_list:
            line = ','.join(words[word])
            f.write(line)
