import re

import numpy as np
import pandas as pd


def clean_hash39(df):
    df.title = df.title.str.replace(' #39;', "'")
    return df


def clean_multiple_whitespace(df):
    df.description = df.description.str.replace(r'\s\s+', ' ', regex=True)
    return df


def clean_trailing_leading(df):
    df.description = df.description.str.replace(' #39;', "'")
    df.description = df.description.str.replace(r'\\', ' ') # 2
    df.description = df.description.str.replace(r'\\\\', ' ') # 180

    df.description = df.description.str.strip(r' \\\n\t\'\"')

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

    df = clean_hash39(df)
    df = clean_multiple_whitespace(df)
    df = clean_trailing_leading(df)

    train_data = df.loc[:120000]
    test_data = df.loc[120000:]

    train_data.to_csv(path + 'cleaned_train.csv', index=False)
    test_data.to_csv(path + 'cleaned_test.csv', index=False)


if __name__ == '__main__':
    main()
