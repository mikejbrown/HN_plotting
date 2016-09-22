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

@author: Michael
"""

import pandas as pd
import numpy as np

def read_data(file_path):
    """
    Reads the data from a csv file, appropriately munging null and missing values
    and assigning category labels.
    Returns: a Pandas dataframe object containing the cleaned data.
    """
    non_numeric_fields = [ 'Diagnosis', 'DxCode', 'T', 'N', 'Side', 'Notes']
    category_codes = ['Hypopharynx', 'Nasopharynx', 'Oral', 'Oropharynx', 'Parotid', 'Skin', 'Larynx']

    data = pd.read_csv(file_path)

    # some columns need explicit type conversion to numerics because the csv file
    # has spaces which cause the field to be mis-parsed
    columns_which_need_munging = [c for c in data.columns
                                    if data[c].dtype==np.dtype('O')
                                    and c not in non_numeric_fields]
    for c in columns_which_need_munging:
        data[c] = pd.to_numeric(data[c], errors='coerce')

    # clean 99999 represeting missing data
    data = data.where(data != 99999)

    # mark 'Category' as a categorical variable and label appropriately
    data['Category'] = data['Category'].astype("category")
    data['Category'].cat.categories = category_codes

    data.set_index('Patient')

    return data

def time_points_for_variable(variable):
    """ Returns a list of column names for the time points of a given variable. """
    time_points = ['_B', '_W2', '_W4', '_W6', '_FU1', '_FU3', '_FU6', '_FU12']
    return [variable + tp for tp in time_points]

if __name__ == "__main__":
    data_file_path = "Taste_and_QOL_data.csv"

    data = read_data(data_file_path)

    for c in data.Category.sort_values().unique():
        cat_data = data[data.Category == c]

        print("*** Category: % s ***" % c)
        print(cat_data[time_points_for_variable('Taste')].describe())

    cols = ['Category',]
    cols.extend(time_points_for_variable('Taste'))
