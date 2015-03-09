import pandas as pd
import numpy as np


def load_data(year=2010):
    '''
    Load data into dataframes

    Returns user info, attendance, addresses, relationships
    '''
    # user info dataframe
    dfn = pd.read_csv(
        '/Users/jpaddison/Documents/Zipfian/ProjectData/NANames.csv')
    # attendance dataframe
    path = '/Users/jpaddison/Documents/Zipfian/ProjectData/'
    if (2001 <= year) and (year <= 2002):
        filename = 'Att01-02.csv'
    elif (2003 <= year) and (year <= 2004):
        filename = 'Att03-04.csv'
    elif (2005 <= year) and (year <= 2006):
        filename = 'Att05-06.csv'
    elif (2007 <= year) and (year <= 2008):
        filename = 'Att07-08.csv'
    elif (2009 <= year) and (year <= 2010):
        filename = 'Att09-10.csv'
    elif (2011 <= year) and (year <= 2012):
        filename = 'Att11-12.csv'
    elif (2013 <= year) and (year <= 2015):
        filename = 'Att13-15.csv'
    else:
        raise ValueError('no data for year ' + str(year))
    dfa = pd.read_csv(path + filename)
    # address dataframe
    dfadd = pd.read_csv(
        '/Users/jpaddison/Documents/Zipfian/ProjectData/NAAddresses.csv')
    # relationship dataframe
    dfr = pd.read_csv(
        '/Users/jpaddison/Documents/Zipfian/ProjectData/NARelations.csv')
    return dfn, dfa, dfadd, dfr


def clean_data(dfn, dfa, dfadd):
    '''
    Removes unwanted columns, gets addresses, and fills nans

    Returns user info, attendance
    '''
    # use interesting columns
    useful_cols = ['BirthYear', 'Gender', 'MainAddress', 'NameCounter',
                   'FamNu', 'UnitNu', 'WhenSetup']
    dfn = dfn[useful_cols]
    # merge addresses with info
    dfn = dfn.rename(columns={'MainAddress': 'AddressCounter'})
    dfadd = dfadd[['City', 'AddressCounter']]
    dfn = pd.merge(dfn, dfadd, on='AddressCounter')
    dfn = dfn.drop('AddressCounter', axis=1)
    # fill nans with ridiculous things
    dfn = dfn.fillna({'BirthYear': 1800, 'Gender': 'N', 'City': 'NA Land'})
    return dfn, dfa
