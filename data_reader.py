# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 21:16:23 2016

Data file has fields (* == non-numeric):
    Patient
    AgeatRecruit
    Gender
    *Diagnosis
    *DxCode
    Category
    *T
    *N
    *Side
    *Notes
    Dose
    Fraction
    Chemo
    Modality
    Taste_B
    Taste_W2
    Taste_W4
    Taste_W6
    Taste_FU1
    Taste_FU3
    Taste_FU6
    Taste_FU12
    Taste_W4_diff
    Taste_W6_diff
    Taste_FU1_diff
    Taste_FU3_diff
    Taste_FU6_diff
    Taste_FU12_diff
    filter_$
    Overall_QOL_B
    Overall_QOL_W2
    Overall_QOL_W4
    Overall_QOL_W6
    Overall_QOL_FU1
    Overall_QOL_FU3
    Overall_QOL_FU6
    Overall_QOL_FU12

Missing data value:
    99999

Category codes:
    1 Hypopharynx
    2 Nasopharynx
    3 Oral
    4 Oropharynx
    5 Parotid
    6 Skin
    7 Larynx

Gender codes:
    0 Male
    1 Female

Chemo codes:
    0 No chemo
    1 Chemo

Modality codes:
    1 3D
    2 IMRT

@author: Michael
"""

import pandas as pd
import numpy as np


def output_analysis(results, name, save_analysis, base_path="analysis"):
    """ If save_analysis == True, saves the analysis results as a file of name
    'base_path/name'.
    If save_analysis == False, prints the results to the stdout."""
    if save_analysis:
        import os
        fname = os.path.realpath(os.path.join(base_path, name))
        dname = os.path.dirname(fname)
        if not (os.path.exists(dname) and os.path.isdir(dname)):
            os.mkdir(dname)
        with open(fname, 'w') as file:
            file.write(results)
    else:
        print(results)


def read_data(file_path):
    """
    Reads the data from a csv file, appropriately munging null and missing
    values and assigning category labels.

    Returns: a Pandas dataframe object containing the cleaned data.
    """
    non_numeric_fields = ['Diagnosis', 'DxCode', 'T', 'N', 'Side', 'Notes']
    category_codes = ['Hypopharynx',
                      'Nasopharynx',
                      'Oral',
                      'Oropharynx',
                      'Parotid',
                      'Skin',
                      'Larynx']

    data = pd.read_csv(file_path)

    # Some columns need explicit type conversion to numerics because the csv
    # file has spaces which cause the field to be mis-parsed.
    # NOTE: pylint persistently complains about no member existing, because it
    # is stupid about recognizing pandas objects. Explicitly ignore the linter
    # checks here because _everything is fine_!
    # pylint: disable=E1103
    columns_which_need_munging = [c for c in data.columns
                                  if data[c].dtype == np.dtype('O') and
                                  c not in non_numeric_fields]
    # pylint: enable=E1103
    for col in columns_which_need_munging:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # clean 99999 represeting missing data
    # NOTE: same comment as above about _stupid_ pylint
    # pylint: disable=E1103
    data = data.where(data != 99999)
    # pylint: enable=E1103

    # mark 'Category' as a categorical variable and label appropriately
    data['Category'] = data['Category'].astype("category")
    data['Category'].cat.categories = category_codes

    data['Gender'] = data['Gender'].astype("category")
    data['Gender'].cat.categories = ['Male', 'Female']

    data['Chemo'] = data['Chemo'].astype("category")
    data['Chemo'].cat.categories = ['No chemo', 'Chemo']

    data['Modality'] = data['Modality'].astype("category")
    data['Modality'].cat.categories = ['3D', 'IMRT']

    data.set_index('Patient')

    return data


def time_points_for_variable(variable):
    """ Returns a list of column names for the time points of a variable. """
    time_points = ['_B', '_W2', '_W4', '_W6', '_FU1', '_FU3', '_FU6', '_FU12']
    return [variable + tp for tp in time_points]

if __name__ == "__main__":
    DATA_FILE_PATH = "Taste_and_QOL_data.csv"
    SAVE_ANALYSIS = True

    DATA = read_data(DATA_FILE_PATH)

    for cat in DATA.Category.sort_values().unique():
        cat_data = DATA[DATA.Category == cat]

        print("*** Category: % s ***" % cat)
        print(cat_data[time_points_for_variable('Taste')].describe())

    COLS = ['Category', ]
    COLS.extend(time_points_for_variable('Taste'))
    COLS.extend(time_points_for_variable('Overall_QOL'))

    SUMMARY = DATA[COLS].groupby('Category').describe()
    output_analysis(SUMMARY.to_csv(), 'summary-stats.csv', SAVE_ANALYSIS)
    SUMMARY_HTML = """
    <html>
        <head>
            <title>Summary statistics</title>
        </head>
        <body>
            %s
        </body>
    </html>
    """ % SUMMARY.to_html()
    output_analysis(SUMMARY_HTML, 'summary-stats.html', SAVE_ANALYSIS)

    REDUCE_DATA = DATA.groupby(['Category', 'T', 'N', 'Gender'])
    SUMMARY2 = REDUCE_DATA.size().sort_values(ascending=False).unstack()
    output_analysis(SUMMARY2.to_csv(),
                    'summary-stats-frequency-by-staging.csv',
                    SAVE_ANALYSIS)
    SUMMARY_HTML = """
    <html>
        <head>
            <title>Summary statistics by staging</title>
        </head>
        <body>
            %s
        </body>
    </html>
    """ % SUMMARY2.to_html()
    output_analysis(SUMMARY_HTML,
                    'summary-stats-frequency-by-staging.html',
                    SAVE_ANALYSIS)
