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


def save_data(df):
    path = './adato/data/'

    train_data = df.loc[:120000]
    test_data = df.loc[120000:]

    train_data.to_csv(path + 'cleaned_train.csv', index=False)
    test_data.to_csv(path + 'cleaned_test.csv', index=False)


def main():
    df = import_data()

    data_cleaner = DataCleaner(df)
    data_cleaner.clean_data()
    cleaned_df = data_cleaner.df

    save_data(cleaned_df)


if __name__ == '__main__':
    main()
