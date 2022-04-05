import camelot
import pandas as pd


def main():
    not_processed = 0
    pages = ','.join([str(x) for x in range(1, 67)])
    tables = camelot.read_pdf('data/JN024wordlist.pdf', pages=pages)
    df_list = list()
    count = 1
    for table in tables:
        print('processing table {}'.format(count))
        count += 1

        df = table.df
        df.columns = ['RAW_VOCAB', 'RAW_MEANING']
        df['FURI'] = ''
        df['VOCAB'] = ''
        df['MEANING'] = ''
        for index, row in df.iterrows():
            row['MEANING'] = row['RAW_MEANING'].replace("\n", '').replace(' ', '').strip()
            raw = row['RAW_VOCAB']
            raw = raw.replace('（する）', '').strip()
            parts = raw.split("\n")
            if len(parts) > 4:
                not_processed += 1
                continue

            if len(parts) == 4:
                row['FURI'] = ''.join([parts[0], parts[1]])
                row['VOCAB'] = ''.join([parts[2], parts[3]])
            elif len(parts) == 3:
                row['FURI'] = ''.join([parts[0], parts[2]])
                row['VOCAB'] = ''.join([parts[1], parts[2]])
            elif len(parts) == 2:
                row['FURI'] = parts[0].replace(' ', '')
                row['VOCAB'] = parts[1].replace(' ', '')
            elif len(parts) == 1:
                row['VOCAB'] = parts[0].replace(' ', '')
        df_list.append(df)

    all_df = pd.concat(df_list)
    print(all_df)
    print('not processed words = {}'.format(not_processed))


if __name__ == '__main__':
    main()
