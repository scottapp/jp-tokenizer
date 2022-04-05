import fugashi


def get_i_adjectives(word_list):
    tagger = fugashi.Tagger()
    out_list = list()
    for word in word_list:
        tagged = tagger(word)
        # want to tag just one word only
        if len(tagged) != 1:
            continue
        if tagged[0].feature.cType == '形容詞':
            out_list.append(tagged[0].surface)
    return out_list


def get_na_adjectives(word_list):
    tagger = fugashi.Tagger()
    out_list = list()
    for word in word_list:
        tagged = tagger(word)
        # want to tag just one word only
        if len(tagged) != 1:
            continue
        if tagged[0].feature.pos1 == '形状詞':
            out_list.append(tagged[0].surface)
    return out_list


def get_verbs(word_list):
    tagger = fugashi.Tagger()
    out_list = list()
    for word in word_list:
        tagged = tagger(word)
        # want to tag just one word only
        if len(tagged) != 1:
            continue
        if tagged[0].feature.pos1 == '動詞':
            out_list.append(tagged[0].surface)
    return out_list
