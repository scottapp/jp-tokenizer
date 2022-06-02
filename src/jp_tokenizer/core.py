import fugashi
import jaconv


def convert_furigana(tagger, text):
    words = tagger(text)
    output = list()
    for word in words:
        """
        if word.feature.pos1 in ['名詞']:
            print(word, word.feature.pos1, jaconv.kata2hira(word.feature.kana))
        """
        word_dict = dict()
        word_dict['surface'] = word.surface
        output.append(word_dict)

        if word.feature.goshu == '記号' or word.feature.pos1 == '代名詞' or word.feature.pos2 == '固有名詞':
            continue

        if word.feature.pos1 == '接尾辞' or word.feature.pos2 == '数詞':
            continue

        if not word.feature.kana:
            continue

        hira = jaconv.kata2hira(word.feature.kana)
        if word.feature.kana != '' and hira != word.surface:
            word_dict['furi'] = jaconv.kata2hira(word.feature.kana)
            word_dict['orthBase'] = word.feature.orthBase
            word_dict['hiraBase'] = jaconv.kata2hira(word.feature.kanaBase)
            # '五段-ラ行'
            word_dict['cType'] = word.feature.cType
            # '動詞'
            word_dict['pos1'] = word.feature.pos1
            # '普通名詞', '一般'
            word_dict['pos2'] = word.feature.pos2

    return output


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
