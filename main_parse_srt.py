import os
import json
import pandas as pd
import pickle
import fugashi
from jp_tokenizer.core import convert_furigana


def extract_meaning_example(text, eg_str):
    text = text[0:text.find('//')]
    parts = text.split(eg_str)
    if len(parts) == 1:
        meaning = parts[0].replace('(1)', '').replace('(2)', '').replace('(3)', '').strip()
        return meaning, ''
    meaning = parts[0].replace('(1)', '').replace('(2)', '').replace('(3)', '').strip()
    example = parts[1].strip()
    return meaning, example


def output_verb_groups():
    df = pd.read_pickle('data/compound_verbs.pkl')
    groups = df.groupby('BACKVERB')
    count = 0
    for verb, df in groups:
        if len(df) >= 10:
            count += 1
            df.to_pickle('data/compound_verbs/{:03d}_items_{}.pkl'.format(len(df), verb))
    print(count, 'files created')


def main():
    df = pd.read_excel('data/vv-lexicon-20181018.xlsx')
    new_list = list()
    for index, row in df.iterrows():
        data = dict()
        data['VERB'] = row['漢字表記1'].strip()
        data['YOMI'] = row['よみ'].strip()
        data['TRANSITIVE'] = row['自他'].strip()
        data['BACKVERB'] = row['後項表記'].strip()

        try:
            level = row['基本文型']
            data['N1'] = 0
            data['N2'] = 0
            data['N3'] = 0
            if not pd.isna(level):
                if 'N1' in level:
                    data['N1'] = 1
                if 'N2' in level:
                    data['N2'] = 1
                if 'N3' in level:
                    data['N3'] = 1
        except Exception as ex:
            print(ex)

        data['MEANING_JP'] = ''
        data['EXAMPLE_JP'] = ''
        items = row['意味・用例'].split('|')
        for text in items:
            try:
                meaning, example = extract_meaning_example(text, '例::')
            except Exception as ex:
                print(index, data['VERB'])
                assert False

            if data['MEANING_JP']:
                data['MEANING_JP'] = '{}|{}'.format(data['MEANING_JP'], meaning)
                data['EXAMPLE_JP'] = '{}|{}'.format(data['EXAMPLE_JP'], example)
            else:
                data['MEANING_JP'] = meaning
                data['EXAMPLE_JP'] = example
        data['JP_COUNT'] = len(items)

        data['MEANING_EN'] = ''
        data['EXAMPLE_EN'] = ''
        items = row['英語訳'].split('|')
        for text in items:
            try:
                meaning, example = extract_meaning_example(text, 'E.g.:')
            except Exception as ex:
                print(index, data['VERB'])
                assert False

            if data['MEANING_EN']:
                data['MEANING_EN'] = '{}|{}'.format(data['MEANING_EN'], meaning)
                data['EXAMPLE_EN'] = '{}|{}'.format(data['EXAMPLE_EN'], example)
            else:
                data['MEANING_EN'] = meaning
                data['EXAMPLE_EN'] = example
        data['EN_COUNT'] = len(items)

        data['MEANING_CH'] = ''
        data['EXAMPLE_CH'] = ''
        items = row['中国語（繁体字）訳'].split('|')
        for text in items:
            try:
                meaning, example = extract_meaning_example(text, '例::')
            except Exception as ex:
                print(index, data['VERB'])
                assert False

            if data['MEANING_CH']:
                data['MEANING_CH'] = '{}|{}'.format(data['MEANING_CH'], meaning)
                data['EXAMPLE_CH'] = '{}|{}'.format(data['EXAMPLE_CH'], example)
            else:
                data['MEANING_CH'] = meaning
                data['EXAMPLE_CH'] = example
        data['CH_COUNT'] = len(items)

        if data['JP_COUNT'] != data['EN_COUNT'] != data['CH_COUNT']:
            print(index, 'error example count')

        if len(items) >= 3:
            print(index, len(items))

        new_list.append(data)

    new_df = pd.DataFrame(new_list)
    print(new_df)

    new_df.to_pickle('data/compound_verbs.pkl')
    print('ok')


def parse_srt_file():
    with open('data/srt/半沢直樹２nd＃01.srt', 'r', encoding='utf-8-sig') as f:
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


def load_dictionary(dir):
    output_map = {}
    files = os.listdir(dir)

    result = list()
    for file in files:
        if file.startswith('term'):
            with open('data/jmdict/%s'%file, 'r', encoding='utf8') as f:
                data = f.read()
                #d = json.loads(data.decode("utf-8"))
                d = json.loads(data)
                result.extend(d)

    for entry in result:
        if entry[0] in output_map:
            output_map[entry[0]].append(entry)
        else:
            # Using headword as key for finding the dictionary entry
            output_map[entry[0]] = [entry]
    return output_map


def convert_dict():
    d = load_dictionary('data/jmdict')
    with open('data/jmdict.pkl', 'wb') as handle:
        pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    with open('data/jmdict.pkl', 'rb') as handle:
        jmdict = pickle.load(handle)

    n1, n2, n3 = get_compound_verbs_tables()

    tagger = fugashi.Tagger()
    lines = parse_srt_file()
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
                try:
                    if info:
                        item['side_b'] = info[0][5][0]
                    else:
                        item['side_b'] = "meaning unknown"
                except Exception as ex:
                    print(ex)
                    print(vocab)
                    print(info)
                    assert False

            tmp.append(item['surface'])
            furi = item.get('furi', None)
            if furi:
                tmp.append('<ruby>{}</ruby>'.format(furi))

        #print(tmp)
        print(converted)
        content.append(converted)

    print(len(n1_vocabs))
    print(len(n2_vocabs))
    print(len(n3_vocabs))

    out_file = dict()
    out_file['content'] = content
    out_file['n1_vocabs'] = n1_vocabs
    out_file['n2_vocabs'] = n2_vocabs
    out_file['n3_vocabs'] = n3_vocabs
    with open('data/content.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(out_file, indent=2, ensure_ascii=False))
