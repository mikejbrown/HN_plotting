# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 19:57:57 2016

Create a synthetic CSV data file in the format:

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

from data_reader import output_analysis


def prepare_synthetic_data(num_patients=100, seed=534454546):
    """ Prepare a synthetic data set to mimic the real one for testing. """
    num_pts = num_patients
    np.random.seed(seed)
    data = pd.DataFrame({'Patient': pd.Series(np.arange(1, num_pts+1))})
    data['AgeatRecruit'] = pd.Series(np.random.randint(40, 80+1, size=num_pts))
    data['Dose'] = pd.Series(np.random.random_sample(size=num_pts) * 15 + 60)
    data['Fraction'] = pd.Series(np.random.randint(30, 36+1, size=num_pts))

    boolean_fields = "Gender Chemo Modality filter_$".split()
    for field in boolean_fields:
        data[field] = pd.Series(np.random.choice([0, 1], size=num_pts))
    data['Modality'] += 1
    data['Category'] = np.random.choice([1, 2, 3, 4, 5, 6, 7], size=num_pts)

    data['Side'] = np.random.choice(['Bilateral',
                                     'Left',
                                     'Not Paired',
                                     'Right'],
                                    size=num_pts)

    idx = (data['Side'] == 'Left') | (data['Side'] == 'Right')
    data['Notes'] = np.array([' ', ] * num_pts)
    data['Notes'][idx] = np.random.choice([' ', ' ', ' ', 'Ipsilateral'],
                                          idx.value_counts()[True])
    data['Diagnosis'] = np.random.choice(['Gum',
                                          'Lignual tonsil',
                                          'Nasopharynx',
                                          'Skin',
                                          'Tonsil',
                                          'Tonsillar pillar',
                                          'Uvula',
                                          'ant tongue part unsp',
                                          'base of tongue',
                                          'border of tongue',
                                          'glottis',
                                          'hypopharynx',
                                          'larynx',
                                          'lat floor of mouth',
                                          'lip unspecified',
                                          'mouth other',
                                          'nasopharynx',
                                          'oropharynx',
                                          'oropharynx unsp',
                                          'parotid',
                                          'post cricoid',
                                          'post wall hypopharynx',
                                          'pyriform sinus',
                                          'scalp & neck',
                                          'skin',
                                          'skin of scalp & neck',
                                          'skin oth/unsp parts face',
                                          'skin unspecified',
                                          'soft palate',
                                          'subglottis',
                                          'supraglottis',
                                          'tongue',
                                          'tonsil',
                                          'tonsil unspecified',
                                          'tonsillar fossa',
                                          'unknown primary',
                                          'vallecula',
                                          'wo site specification'],
                                         size=num_pts)
    data['DxCode'] = np.random.choice(['C00', 'C01', 'C02', 'C03', 'C04',
                                       'C05', 'C06', 'C07', 'C09', 'C10',
                                       'C11', 'C12', 'C13', 'C32', 'C33',
                                       'C44', 'C80'], size=num_pts)
    data['T'] = np.random.choice(['T1', 'T2', 'T3', 'T4', 'T4a', 'T4b', 'Tx'],
                                 size=num_pts)
    data['N'] = np.random.choice(['N0', 'N1', 'N2', 'N2a', 'N2b', 'N2c', 'N3',
                                  'N3b'], size=num_pts)

    score_fields = """Taste_B
                    Taste_W2
                    Taste_W4
                    Taste_W6
                    Taste_FU1
                    Taste_FU3
                    Taste_FU6
                    Taste_FU12
                    Overall_QOL_B
                    Overall_QOL_W2
                    Overall_QOL_W4
                    Overall_QOL_W6
                    Overall_QOL_FU1
                    Overall_QOL_FU3
                    Overall_QOL_FU6
                    Overall_QOL_FU12""".split()
    for field in score_fields:
        data[field] = pd.Series(np.random.randint(0, 100+1, size=num_pts))
        num_nans_in_field = np.random.choice([0, 0, 0, 0, 1, 1, 2])
        indices = np.random.randint(0, num_pts, size=num_nans_in_field)
        data[field].iloc[indices] = np.nan
        num_missing_in_field = np.random.choice([0, 0, 0, 1, 1, 1, 2, 2, 3])
        indices = np.random.randint(0, num_pts, size=num_missing_in_field)
        data[field].iloc[indices] = 99999
    data.fillna(value=' ')

    data['Taste_W4_diff'] = data.Taste_W2 - data.Taste_W4
    data['Taste_W6_diff'] = data.Taste_W2 - data.Taste_W6
    data['Taste_FU1_diff'] = data.Taste_W2 - data.Taste_FU1
    data['Taste_FU3_diff'] = data.Taste_W2 - data.Taste_FU3
    data['Taste_FU6_diff'] = data.Taste_W2 - data.Taste_FU6
    data['Taste_FU12_diff'] = data.Taste_W2 - data.Taste_FU12

    data.set_index('Patient')

    return data

if __name__ == "__main__":
    RESULTS = prepare_synthetic_data().to_csv()

    output_analysis(RESULTS, "synthetic-data.csv", True, base_path='data')
