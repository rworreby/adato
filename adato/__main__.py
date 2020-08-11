import pandas as pd
from flair.data import Corpus
from flair.datasets import CSVClassificationCorpus
from flair.embeddings import WordEmbeddings, DocumentRNNEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer

# import keras


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


def main():
    # df = import_data()
    # print(df)

    data_folder = './adato/data/'
    column_name_map = {0: 'label_topic', 2: 'text'}

    corpus: Corpus = CSVClassificationCorpus(data_folder,
                                             column_name_map,
                                             train_file='cleaned_train.csv',
                                             test_file='cleaned_test.csv',
                                             skip_header=True,
                                             delimiter=',',
                                             )

    print(corpus)
    print(corpus.train[0])

    label_dict = corpus.make_label_dictionary()

    word_embeddings = [WordEmbeddings('glove')]
    document_embeddings = DocumentRNNEmbeddings(word_embeddings,
                                                hidden_size=256,
                                                )

    classifier = TextClassifier(document_embeddings,
                                label_dictionary=label_dict,
                                )

    trainer = ModelTrainer(classifier, corpus)

    trainer.train('adato/model/classifiers/flair/',
                  learning_rate=0.1,
                  mini_batch_size=32,
                  anneal_factor=0.5,
                  patience=5,
                  max_epochs=150)


if __name__ == '__main__':
    main()
