'''
Feature engineering functions
'''
import pandas as pd
import numpy as np
from collections import defaultdict
import datetime
import utilities


def select_active(dfn, dfa, today):
    '''
    Select active users, defined as coming twice in the last two months

    Returns user info, attendance
    '''
    # select for year for speed
    dfa = dfa[dfa['Date'].str[-4:] == str(today.year)]

    two_months = np.timedelta64(2, 'M')
    recent_sundays = (dfa['Organization'] == 'Sunday Worship') & \
                     (pd.to_datetime(dfa['Date']) >= today - two_months) & \
                     (pd.to_datetime(dfa['Date']) < today)
    recent_attendance_numbers = dfa[recent_sundays]\
        .groupby(['NameID'])['Date'].nunique()
    recent_users = recent_attendance_numbers[
        recent_attendance_numbers >= 2].index

    solid_users = set(recent_users)
    # solid user info
    solid_users_arr = np.array(list(solid_users))
    dfn = dfn[np.in1d(dfn['NameCounter'], solid_users_arr)]
    # Some users are not in dfn, which is, hmm, bad
    lonelies = solid_users_arr[~np.in1d(solid_users_arr, dfn.index)]

    # solid user attendance
    dfa = dfa[dfa['NameID'].isin(solid_users)]

    # There are more intelligent places for this, but this is the fastest
    dfa['Date'] = pd.to_datetime(dfa['Date'])
    return dfn, dfa


def add_churn(dfn, dfa, today):
    '''
    Add a churn column for people who do not come in the next two months

    Returns user info
    '''
    future_present_users = dfa[
        (pd.to_datetime(dfa['Date']) >= today) &
        (pd.to_datetime(dfa['Date']) <= today + np.timedelta64(2, 'M')) &
        (dfa['Organization'] == 'Sunday Worship')]['NameID'].values
    dfn['churn'] = pd.Series((~dfn['NameCounter'].isin(future_present_users))
                             .astype('int'), index=dfn.index)
    return dfn


def add_recent_attendance(dfn, dfa, today):
    '''
    Adds attendance per Sunday for the last n sundays

    Returns user info
    '''

    sunday = today - np.timedelta64(today.dayofweek + 1, 'D')

    for i in xrange(1, 9):
        present_users = dfa[
            (dfa['Date'] == sunday) &
            (dfa['Organization'] == 'Sunday Worship')]['NameID'].values
        dfn['t-' + str(i)] = 0
        dfn['t-' + str(i)] = pd.Series(
            dfn['NameCounter'].isin(present_users).astype('int'),
            index=dfn.index)
        sunday -= np.timedelta64(7, 'D')

    return dfn


def small_group_percentage(user_and_sg, dfa=None, sg_dates=None, today=None):
    if np.any(pd.isnull(user_and_sg['SmallGroups'])):
        return -1
    dfa_user = dfa[dfa['NameID'] == user_and_sg['NameCounter']]
    att_number = 0
    total_meeting_number = 0
    for sg in user_and_sg['SmallGroups']:
        dfa_user_smallgroup_att = dfa_user[
            (dfa_user['Organization'] == sg) &
            (pd.to_datetime(dfa['Date']) >= today -
             np.timedelta64(4, 'M')) &
            (pd.to_datetime(dfa['Date']) < today)]
        att_number += len(dfa_user_smallgroup_att['Date'].unique())
        total_meeting_number += len(sg_dates[sg])
    return att_number / float(total_meeting_number) * 100


def add_small_groups(dfn, dfa, today):
    '''
    Adds small group membership and attendance columns

    Returns user info
    '''
    small_group_users = dfa[
        (pd.to_datetime(dfa['Date']) >= today - np.timedelta64(4, 'M')) &
        (pd.to_datetime(dfa['Date']) < today) &
        (dfa['Organization'] != 'Sunday Worship')]['NameID'].values
    dfn['InSG'] = 0
    dfn['InSG'] = pd.Series(
        dfn['NameCounter'].isin(small_group_users).astype('int'),
        index=dfn.index)

    dfsg = dfa[(dfa['Organization'] != 'Sunday Worship') &
               (dfa['Organization'] != 'Sunday School') &
               (pd.to_datetime(dfa['Date']) >= today - np.timedelta64(4, 'M')) &
               (pd.to_datetime(dfa['Date']) < today)]
    sg_series = dfsg.groupby('NameID')['Organization'].unique()
    dfsg = pd.DataFrame({'NameCounter': sg_series.index,
                         'SmallGroups': sg_series})
    dfn = pd.merge(dfn, dfsg, how='left', on='NameCounter')

    sg_dates = {}
    for small_group in dfa['Organization'].unique():
        if (small_group != 'Sunday Worship') & (small_group != 'Sunday School'):
            sg_dates[small_group] = \
                dfa[(pd.to_datetime(dfa['Date']) >=
                     today - np.timedelta64(4, 'M')) &
                    (pd.to_datetime(dfa['Date']) < today) &
                    (dfa['Organization'] == small_group)]['Date'].unique()

    dfn['SGPercentage'] = dfn[['NameCounter', 'SmallGroups']].apply(
        small_group_percentage, axis=1, dfa=dfa, sg_dates=sg_dates, today=today)

    dfn = dfn.drop('SmallGroups', axis=1)

    return dfn


def add_family(dfn, dfr):
    '''
    Adds a family size column

    Returns user info
    '''
    def find_fam(fam_id, dfn, dfr):
        return len(dfn[dfn['FamNu'] == fam_id])
    dfn['Family'] = dfn['FamNu'].apply(find_fam, dfn=dfn, dfr=dfr)
    return dfn


def to_relative_time(dfn, today):
    '''
    Adds columns for years in church and age from WhenSetup and BirthYear
    '''
    dfn['YearsInChurch'] = today.year - dfn['WhenSetup']
    dfn['Age'] = today.year - dfn['BirthYear']
    return dfn


def add_monthly_ave(dfn, dfa, today):
    month_end = today
    month_begin = today - np.timedelta64(1, 'M')
    for i in xrange(1, 4):
        dfa_month = dfa[(month_begin <= dfa['Date']) &
                        (dfa['Date'] < month_end) &
                        (dfa['Organization'] == 'Sunday Worship')]
        num_sundays = dfa_month['Date'].nunique()
        att_series = dfa_month.groupby('NameID')['Date'].count()
        att_df = pd.DataFrame({'NameCounter': att_series.index,
                              str(i) + 'MonthsAgoAtt': att_series/num_sundays})
        dfn = pd.merge(dfn, att_df, how='left', on='NameCounter')

        dfn = dfn.fillna({str(i) + 'MonthsAgoAtt': 0})

        month_end = month_begin
        month_begin = month_end - np.timedelta64(1, 'M')
    return dfn


def model_prep(dfn):
    '''
    Transforms dataframe into form presentable to a model.

    Returns feature matrix X, labels y, row identifiers name_ids, and the
    modified user info
    '''
    dfn = dfn.drop(['City', 'FamNu', 'UnitNu', 'BirthYear', 'Gender',
                    'WhenSetup'], axis=1) # small groups back in
    dfn = pd.get_dummies(dfn)
    name_ids = dfn.pop('NameCounter').values
    y = dfn.pop('churn').values
    X = dfn.values
    return X, y, name_ids, dfn
