import json
import fugashi
import pickle
from jp_tokenizer.core import convert_furigana


def parse_srt_file():
    with open('data/srt/test.srt', 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    new_block = True
    line_buffer = list()
    output = list()
    for line in lines:
        line = line.strip()
        if line == '':
            new_block = False
            tmp = ''.join(line_buffer)
            #print(tmp)
            output.append(tmp)
            line_buffer = list()
            continue
        if line.isnumeric():
            continue
        if line.startswith('00:') or line.startswith('01:'):
            new_block = True
            continue

        if new_block:
            line_buffer.append(line.replace('', ''))

    return output


def read_words_from_csv(filename):
    with open(filename, 'r', encoding='utf8') as f:
        lines = f.readlines()
    words = list()
    for line in lines:
        cols = line.split(',')
        if cols:
            words.append(cols)
    return words


def get_compound_verbs_tables():
    level = 'n1'
    src_path = 'data/compound_verb_{}.json'.format(level)
    with open(src_path, 'r', encoding='utf8') as f:
        data = json.loads(f.read())
        data = data['data']

    output = dict()
    for i in range(0, len(data)):
        vocab = data[i]
        output[vocab['side_a']] = vocab

    n1 = output

    level = 'n2'
    src_path = 'data/compound_verb_{}.json'.format(level)
    with open(src_path, 'r', encoding='utf8') as f:
        data = json.loads(f.read())
        data = data['data']

    output = dict()
    for i in range(0, len(data)):
        vocab = data[i]
        output[vocab['side_a']] = vocab

    n2 = output

    level = 'n3'
    src_path = 'data/compound_verb_{}.json'.format(level)
    with open(src_path, 'r', encoding='utf8') as f:
        data = json.loads(f.read())
        data = data['data']

    output = dict()
    for i in range(0, len(data)):
        vocab = data[i]
        output[vocab['side_a']] = vocab

    n3 = output
    return n1, n2, n3


def convert_jp_text(input_text):
    with open('data/jmdict.pkl', 'rb') as handle:
        jmdict = pickle.load(handle)

    n1, n2, n3 = get_compound_verbs_tables()

    tagger = fugashi.Tagger()
    lines = input_text
    n1_vocabs = dict()
    n2_vocabs = dict()
    n3_vocabs = dict()
    content = list()
    for line in lines:
        converted = convert_furigana(tagger, line)
        tmp = list()
        for item in converted:
            vocab = None

            if item.get('orthBase', None):
                vocab = item['orthBase']
            else:
                vocab = item['surface']

            if vocab in n1:
                item['side_b'] = n1[vocab]['side_b']
                n1_vocabs[vocab] = item
            elif vocab in n2:
                item['side_b'] = n2[vocab]['side_b']
                n2_vocabs[vocab] = item
            elif vocab in n3:
                item['side_b'] = n3[vocab]['side_b']
                n3_vocabs[vocab] = item
            elif 'cType' in item or 'pos1' in item:
                info = jmdict.get(vocab, None)
                if not info and item.get('lemma', None):
                    info = jmdict.get(item['lemma'], None)
                try:
                    if info:
                        item['side_b'] = info[0][5][0]
                    else:
                        item['side_b'] = "{}, unknown".format(item.get('lemma', ''))
                except Exception as ex:
                    print(ex)
                    print(vocab)
                    print(item)
                    print(info)
                    assert False

            tmp.append(item['surface'])
            furi = item.get('furi', None)
            if furi:
                tmp.append('<ruby>{}</ruby>'.format(furi))

        print(converted)
        content.append(converted)

    """
    print(len(n1_vocabs))
    print(len(n2_vocabs))
    print(len(n3_vocabs))
    """

    out_file = dict()
    out_file['content'] = content
    out_file['n1_vocabs'] = n1_vocabs
    out_file['n2_vocabs'] = n2_vocabs
    out_file['n3_vocabs'] = n3_vocabs
    return out_file
