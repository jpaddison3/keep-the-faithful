import pandas as pd
import numpy as np

def load_data():
    '''
    Load data into dataframes

    Returns user info, attendance, addresses, relationships
    '''
    # user info dataframe
    dfn = pd.read_csv('/Users/jpaddison/Documents/Zipfian/ProjectData/NANames.csv')
    # attendance dataframe
    dfa = pd.read_csv(
        '/Users/jpaddison/Documents/Zipfian/ProjectData/Att09-10.csv')
    # address dataframe
    dfadd = pd.read_csv(
        '/Users/jpaddison/Documents/Zipfian/ProjectData/NAAddresses.csv')
    # relationship dataframe
    dfr = pd.read_csv(
        '/Users/jpaddison/Documents/Zipfian/ProjectData/NARelations.csv')
    return dfn, dfa, dfadd, dfr


def clean_data(dfn, dfa, dfadd):
    # use interesting columns
    useful_cols = ['BirthYear', 'Gender', 'MainAddress', 'NameCounter',
                   'WhenSetup']
    dfn = dfn[useful_cols]
    # merge addresses with info
    dfn = dfn.rename(columns={'MainAddress': 'AddressCounter'})
    dfadd = dfadd[['City', 'AddressCounter']]
    dfn = pd.merge(dfn, dfadd, on='AddressCounter')
    dfn = dfn.drop('AddressCounter', axis=1)
    # fill nans with ridiculous things
    dfn = dfn.fillna({'BirthYear': 1800, 'Gender': 'N', 'City': 'NA Land'})
    return dfn, dfa