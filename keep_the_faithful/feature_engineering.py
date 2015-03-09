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

    recent_sundays = (dfa['Organization'] == 'Sunday Worship') & \
                     (pd.to_datetime(dfa['Date']) >=
                      today - np.timedelta64(2, 'M')) & \
                     (pd.to_datetime(dfa['Date']) < today)
    recent_attendance_numbers = dfa[recent_sundays]\
        .groupby(['NameID'])['Date'].nunique()
    recent_users = recent_attendance_numbers[
        recent_attendance_numbers >= 2].index

    year_attendance_numbers = dfa[dfa['Organization'] == 'Sunday Worship']\
        .groupby(['NameID'])['Date'].nunique()
    year_users = year_attendance_numbers[year_attendance_numbers >= 2].index

    solid_users = set(recent_users)
    # solid user info
    solid_users_arr = np.array(list(solid_users))
    dfn = dfn[np.in1d(dfn['NameCounter'], solid_users_arr)]
    # Some users are not in dfn, which is, hmm, bad
    lonelies = solid_users_arr[~np.in1d(solid_users_arr, dfn.index)]
    # for l in lonelies:
    #     print l in dfn.index
    #     print l in dfa['NameID'].values

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
    dfn['churn'] = 0
    dfn['churn'] = pd.Series((~dfn['NameCounter'].isin(future_present_users))
                             .astype('int'), index=dfn.index)
    print 'total churned', dfn['churn'].sum()
    print 'churn percentage', 100 * dfn['churn'].mean()
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
               (pd.to_datetime(dfa['Date']) >= today - np.timedelta64(4, 'M')) &
               (pd.to_datetime(dfa['Date']) < today)]
    sg_series = dfsg.groupby('NameID')['Organization'].unique()
    dfsg = pd.DataFrame({'NameCounter': sg_series.index,
                         'SmallGroups': sg_series})
    dfn = pd.merge(dfn, dfsg, how='left', on='NameCounter')

    sg_dates = {}
    for small_group in dfa['Organization'].unique():
        if small_group != 'Sunday Worship':
            sg_dates[small_group] = \
                dfa[(pd.to_datetime(dfa['Date']) >=
                     today - np.timedelta64(4, 'M')) &
                    (pd.to_datetime(dfa['Date']) < today) &
                    (dfa['Organization'] == small_group)]['Date'].unique()

    def small_group_percentage(user_and_sg, today=None):
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

    dfn['SGPercentage'] = dfn[['NameCounter', 'SmallGroups']].apply(
        small_group_percentage, axis=1, today=today)

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


def model_prep(dfn, today):
    '''
    Transforms dataframe into form presentable to a model.

    Returns feature matrix X, labels y, row identifiers name_ids, and the
    modified user info
    '''
    dfn['WhenSetup'] = pd.to_datetime(dfn['WhenSetup'])\
        .apply(lambda x: x.year)
    dfn = to_relative_time(dfn, today)
    dfn = dfn.drop(['City', 'FamNu', 'UnitNu', 'SmallGroups', 'BirthYear', 
                    'WhenSetup'], axis=1)
    dfn = pd.get_dummies(dfn)
    name_ids = dfn.pop('NameCounter').values
    y = dfn.pop('churn').values
    X = dfn.values
    return X, y, name_ids, dfn

if __name__ == '__main__':
    t0 = datetime.datetime.now()
    dfn, dfa, dfadd, dfr = utilities.load_data()
    t1 = datetime.datetime.now() - t0
    print 't1', t1
    dfn, dfa = utilities.clean_data(dfn, dfa, dfadd)
    t2 = datetime.datetime.now() - t0 - t1
    print 't2', t2
    dfn, dfa = select_active(dfn, dfa)
    t3 = datetime.datetime.now() - t0 - t2
    print 't3', t3
    # dfn = add_churn(dfn, dfa)
    # t4 = datetime.datetime.now() - t0 - t3
    # print 't4', t4
    dfn = add_recent_attendance(dfn, dfa)
    t4 = datetime.datetime.now() - t0 - t3
    print 't4', t4
    print dfn.head()
