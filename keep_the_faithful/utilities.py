import pandas as pd
import numpy as np
import utilities
import feature_engineering


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


def full_load(today):
    '''
    Load data frame and add feature engineered columns

    Returns user info
    '''
    dfn, dfa, dfadd, dfr = load_data(today.year)
    dfn, dfa = clean_data(dfn, dfa, dfadd)
    dfn, dfa = feature_engineering.select_active(dfn, dfa, today)
    dfn = feature_engineering.add_churn(dfn, dfa, today)
    dfn = feature_engineering.add_recent_attendance(dfn, dfa, today)
    dfn = feature_engineering.add_small_groups(dfn, dfa, today)
    dfn = feature_engineering.add_family(dfn, dfr)
    dfn['WhenSetup'] = pd.to_datetime(dfn['WhenSetup']).apply(lambda x: x.year)
    dfn = feature_engineering.to_relative_time(dfn, today)
    return dfn


def combine_load(dates):
    '''
    Load feature engineered dataframes for the specified dates

    Returns one user info data frame
    '''
    dfn = full_load(dates[0])
    for date in dates[1:]:
        dfn_i = full_load(date)
        dfn = pd.concat([dfn, dfn_i])
    return dfn
