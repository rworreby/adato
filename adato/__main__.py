import argparse

import pandas as pd
from hyperopt import hp
from flair.data import Corpus
from flair.datasets import CSVClassificationCorpus
from flair.embeddings import WordEmbeddings, DocumentRNNEmbeddings
from flair.embeddings import FlairEmbeddings
from flair.hyperparameter.param_selection import SearchSpace, Parameter
from flair.hyperparameter.param_selection import TextClassifierParamSelector
from flair.hyperparameter.param_selection import OptimizationValue
from flair.models import TextClassifier
from flair.trainers import ModelTrainer


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
    my_parser = argparse.ArgumentParser(add_help=True)
    my_parser.add_argument('-ft',
                           '--finetuning',
                           action='store',
                           type=int,
                           required=False)

    args = my_parser.parse_args()

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

    word_embeddings = [WordEmbeddings('glove')]
    document_embeddings = DocumentRNNEmbeddings(word_embeddings,
                                                hidden_size=256,
                                                )

    if args.finetuning:
        search_space = SearchSpace()
        search_space.add(Parameter.EMBEDDINGS, hp.choice, options=[
            [WordEmbeddings('en')],
            [FlairEmbeddings('news-forward'),
             FlairEmbeddings('news-backward'),
             ],
            [document_embeddings],
        ])
        search_space.add(Parameter.HIDDEN_SIZE,
                         hp.choice,
                         options=[32, 64, 128]
                         )
        search_space.add(Parameter.RNN_LAYERS,
                         hp.choice,
                         options=[1, 2]
                         )
        search_space.add(Parameter.DROPOUT,
                         hp.uniform,
                         low=0.0,
                         high=0.5
                         )
        search_space.add(Parameter.LEARNING_RATE,
                         hp.choice,
                         options=[0.05, 0.1, 0.15, 0.2]
                         )
        search_space.add(Parameter.MINI_BATCH_SIZE,
                         hp.choice,
                         options=[8, 16, 32]
                         )

        param_selector = TextClassifierParamSelector(
            corpus,
            False,
            'adato/model/classifiers/hyperopt/',
            'lstm',
            max_epochs=40,
            training_runs=3,
            optimization_value=OptimizationValue.DEV_SCORE
        )

        param_selector.optimize(search_space, max_evals=2)

    else:
        label_dict = corpus.make_label_dictionary()

        classifier = TextClassifier(document_embeddings,
                                    label_dictionary=label_dict,
                                    )

        trainer = ModelTrainer(classifier, corpus)

        trainer.train('adato/model/classifiers/flair/',
                      learning_rate=0.1,
                      mini_batch_size=32,
                      anneal_factor=0.5,
                      patience=5,
                      max_epochs=40)


if __name__ == '__main__':
    main()
