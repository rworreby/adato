import re

import pandas as pd


class DataCleaner():
    """Class facilitating the cleaning and preprocessing of text data."""
    df: pd.DataFrame = pd.DataFrame()

    def __init__(self, df):
        super(DataCleaner, self).__init__()
        self.df = df

    @property
    def get_df(self):
        return self.df

    def clean_data(self):
        self.clean_hashes()
        self.clean_trailing_leading()
        self.clean_title_remarks()
        self.clean_description_remarks()

        self.df.drop_duplicates(subset=['description'], inplace=True)
        self.df.drop_duplicates(subset=['title'], inplace=True)

    def clean_hashes(self):
        self.df.title = self.df.title.str.replace('#36;', "$")
        self.df.title = self.df.title.str.replace(' #39;', "'")
        self.df.description = self.df.description.str.replace('#36;', "$")
        self.df.description = self.df.description.str.replace(' #39;', "'")

        # return self.df

    def clean_trailing_leading(self):
        self.df.title = self.df.title.str.replace(r'\\\\', ' ')
        self.df.title = self.df.title.str.replace(r'\\', ' ')
        self.df.title = self.df.title.str.replace(r'\s\s+', ' ', regex=True)

        self.df.title = self.df.title.str.strip(' \\\n\t\'\"')

        self.df.description = self.df.description.str.replace(r'\\\\', ' ')
        self.df.description = self.df.description.str.replace(r'\\', ' ')
        self.df.description = self.df.description.str.replace(r'\s\s+', ' ',
                                                              regex=True)

        self.df.description = self.df.description.str.strip(' \\\n\t\'\"')

        # return self.df

    def clean_title_remarks(self):
        # title_remark_re = r'(?:.*)\s\((\w*\.?(?:\w+)+)\)$'
        # df['title_remark'] = df['title'].str.extract(title_remark_re)

        def clean_row(row):
            regex = r'(.*)\s\((\w*\.?\s?(?:\w+)+)\)$'
            m = re.search(regex, row)
            if m:
                return m.group(1)
            else:
                return row

        self.df['title'] = self.df['title'].apply(clean_row)
        # return self.df

    def clean_description_remarks(self):
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

        self.df['description'] = self.df['description'].apply(clean_row)
        # return self.df
