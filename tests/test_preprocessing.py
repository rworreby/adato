"""
Unit tests for the preprocessing pipeline
"""

import re
# import string
import pandas as pd

from hypothesis import given, example, assume
from hypothesis import strategies as st
from hypothesis.extra.pandas import data_frames, column

from preprocessing.data_cleaning import clean_hash39


# for i in range(10):
#     print(
#         st.text(
#             alphabet=string.ascii_letters+r' /\\?-^\'"_:',
#             min_size=20,
#         ).example()
#     )

# regex = re.compile(r'(\w{5}\s){5}', re.ASCII)
# for i in range(10):
#     print(
#         st.from_regex(regex).example()
#     )

# for i in range(10):
#     print(data_frames([column(
#         'description',
#         elements=st.text(
#             alphabet=string.ascii_letters+r' #;/\\?-^\'"_:'
#         ),
#         unique=True)
#     ]).example())

# regex = re.compile(r'.* #39;.*', re.ASCII)    # \w{4,7}\s+
# for i in range(10):
#     print(
#         st.from_regex(regex).example()
#     )


# @given(data_frames([column('title',
#                     elements=st.text(
#                         alphabet=string.ascii_letters+r' #;\''
#                     ),
#                     unique=True)
#                     ]))

def clean_hash39(df):
    df.title = df.title.str.replace(' #39;', "'")
    return df


regex = re.compile(r'.* #39;.*', re.ASCII)


@given(input_df=data_frames(
    [column(
        'title',
        elements=st.from_regex(regex),
        unique=True
    )]
))
@example(input_df=pd.DataFrame(
    {'title':
        ['Robin #39; forever super string test.', 'String 1']}
))
def test_clean_hash39(input_df):
    assume(input_df.shape[0] > 0)
    cleaned_df = clean_hash39(input_df)

    # cleaned_df.loc[0] = 'This is Robin #39;s wrong example.'

    for _, row in cleaned_df.iterrows():
        assert ' #39;' not in row.title
