"""
Unit tests for the preprocessing pipeline
"""

import re
# import string
import pandas as pd

from hypothesis import given, example, assume, settings, HealthCheck
from hypothesis import strategies as st
from hypothesis.extra.pandas import data_frames, column

from preprocessing.data_cleaning import clean_hashes
from preprocessing.data_cleaning import clean_trailing_leading
from preprocessing.data_cleaning import clean_title_remarks
from preprocessing.data_cleaning import clean_description_remarks


# Create hypothesis regex examples:
# regex = re.compile(r'.* #39;.*#36;.*', re.ASCII)
# for i in range(10):
#     print(
#         st.from_regex(regex).example()
#     )


regex = re.compile(r'.* #39;.*#36;.*', re.ASCII)


@given(input_df=data_frames(
    [column(
        'title',
        elements=st.from_regex(regex),
        unique=True
        ),
     column(
        'description',
        elements=st.from_regex(regex),
        unique=True
     )]
))
@example(input_df=pd.DataFrame(
    {'title':
        ['Robin #39; test of strings costing #36;200.', '#39;#36;'],
     'description':
        ['Robin #39; test of strings costing #36;200.', '#39;#36;']
     }
))
def test_clean_hashes(input_df):
    assume(input_df.shape[0] > 0)
    cleaned_df = clean_hashes(input_df)

    # Example case breaking the assertion
    # cleaned_df.loc[0] = 'This is Robin #39;s wrong example.'

    for _, row in cleaned_df.iterrows():
        assert ' #39;' not in row.title
        assert '#36;' not in row.title
        assert ' #39;' not in row.description
        assert '#36;' not in row.description


regex = re.compile(r'\s?"*.*\\.*\\\\.*\s{2,5}.*\n?', re.ASCII)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(input_df=data_frames(
    [column(
        'title',
        elements=st.from_regex(regex),
        unique=True
        ),
     column(
        'description',
        elements=st.from_regex(regex),
        unique=True
        ),
     column(
        'not_tested',
        elements=st.from_regex(regex),
        unique=True
        ),
     ]
))
@example(input_df=pd.DataFrame(
    {'title':
        [r'  String with empty start',
         r'"String starting with "',
         r'String ending with newline character\n',
         r'String with multiple     whitespaces.',
         r'String with \\ backslashes \\\\ in two locations.',
         ],
     'description':
        [r'  String with empty start',
         r'"String starting with "',
         r'String ending with newline character\n',
         r'String with multiple     whitespaces.',
         r'String with \\ backslashes \\\\ in two locations.',
         ]
     }
))
def test_clean_trailing_leading(input_df):
    assume(input_df.shape[0] > 0)
    cleaned_df = clean_trailing_leading(input_df)

    # Example case breaking the assertion
    # cleaned_df.loc[0, 'title'] = '\tTab started string'

    for _, row in cleaned_df.iterrows():
        if row.title:
            assert r'  ' not in row.title
            assert r'\\' not in row.title
            assert r'\\\\' not in row.title
            assert row.title[0] not in ('\n\t\"\' \\')
            assert row.title[-1] not in ('\n\t\"\' \\')
        if row.description:
            assert r'  ' not in row.description
            assert r'\\' not in row.description
            assert r'\\\\' not in row.description
            assert row.description[0] not in ('\n\t\"\' \\')
            assert row.description[-1] not in ('\n\t\"\' \\')


regex = re.compile(r'^.*\s\((\w+\s\w+)?(\w+)?\)$', re.ASCII)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(input_df=data_frames(
    [column(
        'title',
        elements=st.from_regex(regex),
        unique=True
        ),
     column(
        'description',
        elements=st.from_regex(regex),
        unique=True
     )]
))
@example(input_df=pd.DataFrame(
    {'title':
        ['Some News (Blick)', 'Other news (20 Minuten)'],
     'description':
        ['This just happened ...', 'This as well ...']
     }
))
def test_clean_title_remarks(input_df):
    assume(input_df.shape[0] > 0)
    cleaned_df = clean_title_remarks(input_df)

    # Example cases breaking the assertion
    # cleaned_df.loc[0] = 'Some Place like this (Blick)'

    regexes = [
                r'^.*\s\(\w+(\s\w+)?\)$',
                ]
    for _, row in cleaned_df.iterrows():
        for regex in regexes:
            assert not re.match(regex, row.title)


regex = re.compile(r'''^
                        (\w+)?
                        (\.\w+\s)?
                        (,\s\w+\s)?
                        (/\w+\s)?
                        (\w+)?
                        (\s\(\w+\))?
                        \s-{1,2}\s.*
                    ''',
                   re.ASCII | re.X | re.M)


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(input_df=data_frames(
    [column(
        'title',
        elements=st.from_regex(regex),
        unique=True
        ),
     column(
        'description',
        elements=st.from_regex(regex),
        unique=True
     )]
))
@example(input_df=pd.DataFrame(
    {'title':
        [
            str(i) for i in range(10)
        ],
     'description':
        [
            'If you think you may ...',
            'Reuters - Short-sellers ...',
            'Reuters -- Short-sellers ...',
            'Forbes.com - After earning ...',
            'NEW YORK (Reuters) - Short-sellers ...',
            'TEHRAN (Reuters) - OPEC can ...',
            'WASHINGTON/NEW YORK (Reuters) - The auction ...',
            'NAJAF, Iraq - U.S. tanks and ...',
            'CARACAS, Venezuela (Reuters) - Venezuelans crowded ...',
            'OTTAWA (CP) - Canada\'s police ...',
         ]
     }
))
def test_clean_description_remarks(input_df):
    assume(input_df.shape[0] > 0)
    cleaned_df = clean_description_remarks(input_df)

    # Example cases breaking the assertion
    # cleaned_df.loc[0] = 'Some, Place (Blick) - Yet another news ...'
    # cleaned_df.loc[1] = 'Some Place - Yet another news ...'

    regexes = [
                r'^(\w+\s){1,2}-{1,2}\s.*',             # Word -
                r'^\w+\s(\w+\s)?(\(\w+\))?-{1,2}\s.*',  # Word (Word) -
                r'^\w+/\w+(\s\w+)?\s-{1,2}\s.*',        # Word/Word -
                r'^\w+,\s\w+\s(\(\w+\)\s)?-{1,2}\s.*',  # Word, Word -
                r'^\w+\.\w+\s(\(\w+\)\s)?-{1,2}\s.*',   # Word.Word -
                ]
    for _, row in cleaned_df.iterrows():
        for regex in regexes:
            assert not re.match(regex, row.description)
