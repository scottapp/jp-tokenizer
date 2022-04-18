import pandas as pd


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


if __name__ == '__main__':

    #output_verb_groups()
    main()
