import string

# import numpy as np
import pandas as pd

# import keras

# import spacy
# from spacy.lang.en import English

# STOPLIST = set(stopwords.words('english') + list(ENGLISH_STOP_WORDS))
SYMBOLS = " ".join(string.punctuation).split(" ") + ["-", "...", "”", "”"]


def import_data():
    path = './adato/data/'

    train_df = pd.read_csv(
        path + 'cleaned_train.csv',
        header=0,
        names=['classid', 'title', 'description'],
    )
    test_df = pd.read_csv(
        path + 'cleaned_test.csv',
        header=0,
        names=['classid', 'title', 'description'],
    )

    df = pd.concat([train_df, test_df])
    df.reset_index(inplace=True, drop=True)

    return df


"""
def tokenize_text(sample):
    # tokens = parser(sample)
    lemmas = []
    for tok in tokens:
        lemmas.append(tok.lemma_.lower().strip() if tok.lemma_ != "-PRON-"
                      else tok.lower_)

    tokens = lemmas
    tokens = [tok for tok in tokens if tok not in STOPLIST]
    tokens = [tok for tok in tokens if tok not in SYMBOLS]
    return tokens
"""


def main():
    df = import_data()
    print(df)

    # nlp = spacy.load('en_core_web_sm')
    # nlp(df)

    # print(tokenize_text(nlp(df.loc[0, 'description'])))


if __name__ == '__main__':
    main()
