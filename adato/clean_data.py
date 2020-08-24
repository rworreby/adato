import argparse

import pandas as pd

from preprocessing.data_cleaning import DataCleaner


def import_data():
    path = './adato/data/'

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

    return df


def save_data(df, split=None):
    path = './adato/data/'

    train_data = df.loc[:120000]
    test_data = df.loc[120000:]
    # train_data.reset_index(inplace=True, drop=True)
    # test_data.reset_index(inplace=True, drop=True)

    small_train_data = train_data[:split]
    small_test_data = test_data[:split]
    remaining_train_data = train_data[split:]
    remaining_test_data = test_data[split:]

    print(small_train_data.shape)
    print(small_test_data.shape)
    print(remaining_train_data.shape)
    print(remaining_test_data.shape)

    small_train_data.to_csv(path + 'cleaned_train.csv', index=False)
    small_test_data.to_csv(path + 'cleaned_test.csv', index=False)
    remaining_train_data.to_csv(path + 'remaining_cleaned_train.csv',
                                index=False)
    remaining_test_data.to_csv(path + 'remaining_cleaned_test.csv',
                               index=False)


def main():
    my_parser = argparse.ArgumentParser(add_help=True)
    my_parser.add_argument('-s',
                           '--split',
                           action='store',
                           type=int,
                           required=False)

    args = my_parser.parse_args()

    df = import_data()

    data_cleaner = DataCleaner(df)
    data_cleaner.clean_data()
    cleaned_df = data_cleaner.df

    save_data(cleaned_df, args.split)


if __name__ == '__main__':
    main()
