import re

import pandas as pd


def clean_hashes(df):
    df.title = df.title.str.replace('#36;', "$")
    df.title = df.title.str.replace(' #39;', "'")
    df.description = df.description.str.replace('#36;', "$")
    df.description = df.description.str.replace(' #39;', "'")

    return df


def clean_trailing_leading(df):
    df.title = df.title.str.replace(r'\\\\', ' ')
    df.title = df.title.str.replace(r'\\', ' ')
    df.title = df.title.str.replace(r'\s\s+', ' ', regex=True)

    df.title = df.title.str.strip(' \\\n\t\'\"')

    df.description = df.description.str.replace(r'\\\\', ' ')
    df.description = df.description.str.replace(r'\\', ' ')
    df.description = df.description.str.replace(r'\s\s+', ' ', regex=True)

    df.description = df.description.str.strip(' \\\n\t\'\"')

    return df


def clean_title_remarks(df):
    # title_remark_re = r'(?:.*)\s\((\w*\.?(?:\w+)+)\)$'
    # df['title_remark'] = df['title'].str.extract(title_remark_re)

    def clean_row(row):
        regex = r'(.*)\s\((\w*\.?\s?(?:\w+)+)\)$'
        m = re.search(regex, row)
        if m:
            return m.group(1)
        else:
            return row

    df['title'] = df['title'].apply(clean_row)
    return df


def clean_description_remarks(df):
    def clean_row(row):
        regex = r'''^
                    \w+
                    (?:\s\w+)?
                    (?:,\s)?
                    (?:/\w+\s?\w+)?
                    (?:\.?\w+)?
                    (?:\s\(\w+\))?
                    (?:\s-{1,2}\s)+
                    (.*)
                 '''
        m = re.search(regex, row, re.M | re.X)
        if m:
            return m.group(1)
        else:
            return row

    df['description'] = df['description'].apply(clean_row)
    return df


def main():
    path = '../data/'

    train_df = pd.read_csv(
        path + 'train.csv',
        header=0,
        names=['classid', 'title', 'description'],
    )
    test_df = pd.read_csv(
        path + 'test.csv',
        header=0,
        names=['classid', 'title', 'description'],
    )

    df = pd.concat([train_df, test_df])
    df.reset_index(inplace=True, drop=True)

    df = clean_hashes(df)
    df = clean_trailing_leading(df)

    df = clean_title_remarks(df)

    df = clean_description_remarks(df)

    df.drop_duplicates(subset=['description'], inplace=True)
    df.drop_duplicates(subset=['title'], inplace=True)

    train_data = df.loc[:120000]
    test_data = df.loc[120000:]

    train_data.to_csv(path + 'cleaned_train.csv', index=False)
    test_data.to_csv(path + 'cleaned_test.csv', index=False)


if __name__ == '__main__':
    main()
