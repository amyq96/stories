import pandas as pd
import re
import numpy as np

def reformat(df):
    '''
    Reads in an unformated df. Returns a df with an added ward column for each precinct and deletes irrelevent rows
    '''
    df['precinct'] = df['precinct'].astype(str)
    ward = []

    for value in df['precinct']:
        if ('Ward' in value) or ('WARD' in value):
            ward_number = re.findall(r'\d+', value)[0]
            ward.append(ward_number)
        else:
            ward.append(np.nan)

    df['ward'] = ward

    df['ward'] = df['ward'].fillna(method='ffill')

    df = df[~df['precinct'].str.contains('Ward')]
    df = df[~df['precinct'].str.contains('Total')]
    df = df[~df['precinct'].str.contains('Precinct')]
    df = df[~df['precinct'].str.contains('nan')]
    df = df[~df['precinct'].str.contains('WARD')]

    return df

def joinkey(df):
    '''
    Reads in a foramtted df. Adds a ward_precinct style joinkey.
    '''
    df['ward_precinct'] = df['ward'].astype(
        str) + '_' + df['precinct'].astype(str)

    return df