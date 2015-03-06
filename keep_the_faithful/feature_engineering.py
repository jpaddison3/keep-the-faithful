import pandas as pd
import numpy as np
import datetime
import utilities

def select_active(dfn, dfa):
    # select for year for speed
    explore_year = '2010'
    dfa = dfa[dfa['Date'].str[-4:] == explore_year]
    
    today = pd.to_datetime('10/1/2010')
    recent_sundays = (dfa['Organization'] == 'Sunday Worship') & \
                     (pd.to_datetime(dfa['Date']) >=
                      today - np.timedelta64(2, 'M')) & \
                     (pd.to_datetime(dfa['Date']) < today)
    recent_attendance_numbers = dfa[recent_sundays]\
        .groupby(['NameID'])['Date'].nunique()
    recent_users = recent_attendance_numbers[recent_attendance_numbers >= 2].index

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

    return dfn, dfa


def add_churn(dfn, dfa):
    future_present_users = dfa[
        (pd.to_datetime(dfa['Date']) >= pd.to_datetime('10/1/2010')) &
        (pd.to_datetime(dfa['Date']) <= pd.to_datetime('12/12/2010')) &
        (dfa['Organization'] == 'Sunday Worship')]['NameID'].values
    dfn['churn'] = 0
    dfn['churn'] = pd.Series((~dfn['NameCounter'].isin(future_present_users))
                                 .astype('int'), index=dfn.index)
    print 'churn percentage', 100 * dfn['churn'].mean()
    return dfn


def add_recent_attendance(dfn, dfa):
    present_users = dfa[
        (dfa['Date'] == '9/26/2010') &
        (dfa['Organization'] == 'Sunday Worship')]['NameID'].values
    dfn['t-1'] = 0
    dfn['t-1'] = pd.Series(dfn['NameCounter'].isin(present_users).astype('int'),
                               index=dfn.index)

    present_users = dfa[
        (dfa['Date'] == '9/19/2010') &
        (dfa['Organization'] == 'Sunday Worship')]['NameID'].values
    dfn['t-2'] = 0
    dfn['t-2'] = pd.Series(dfn['NameCounter'].isin(present_users).astype('int'),
                               index=dfn.index)

    present_users = dfa[
        (dfa['Date'] == '9/12/2010') &
        (dfa['Organization'] == 'Sunday Worship')]['NameID'].values
    dfn['t-3'] = 0
    dfn['t-3'] = pd.Series(dfn['NameCounter'].isin(present_users).astype('int'),
                               index=dfn.index)

    present_users = dfa[
        (dfa['Date'] == '9/5/2010') &
        (dfa['Organization'] == 'Sunday Worship')]['NameID'].values
    dfn['t-4'] = 0
    dfn['t-4'] = pd.Series(dfn['NameCounter'].isin(present_users).astype('int'),
                               index=dfn.index)

    return dfn

    # # small_group_users = su_att[
    # #     (su_att['Date'] >= today - np.timedelta64(4, 'M')) &
    # #     (su_att['Date'] < today) &
    # #     (su_att['Organization'] != 'Sunday Worship')]['NameID'].values
    # # su_info['InSG'] = 0
    # # su_info['InSG'] = pd.Series(
    # #     su_info['NameCounter'].isin(small_group_users).astype('int'), 
    # #     index=su_info.index)

    # # su_info['SmallGroups'] = None
    # # dfsg = dfa[dfa['Organization'] != 'Sunday Worship']
    # # su_info['SmallGroups'] = dfsg.groupby('NameID')['Organization'].unique()

    # # sg_dates = {}
    # # for small_group in dfa['Organization'].unique():
    # #     if small_group != 'Sunday Worship':
    # #         sg_dates[small_group] = \
    # #             dfa[dfa['Organization'] == small_group]['Date'].unique()
    
    # # def small_group_percentage(small_groups):
    # #     for small_group in small_groups:
    # #         dfa[(dfa['NameID'] == small_groups.index)]

    # # su_info['SGPercentage'] = su_info['SmallGroups'].apply(
    # #     small_group_percentage)

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

# # ------------- Ready the features for model ------------ #
# # change when setup to only use year ## NEED FIXING
# dfn['WhenSetup'] = pd.to_datetime(dfn['WhenSetup'])\
#     .apply(lambda x: x.year)
# su_info = su_info.drop(['City'], axis=1)
# su_info['WhenSetup'] = pd.to_datetime(su_info['WhenSetup'])\
#     .apply(lambda x: x.year)
# su_info = pd.get_dummies(su_info)
# y = su_info.pop('churn').values
# X = su_info.values
# if __name__ == '__main__':
#     dfa, dfn, dfadd, dfr = load_all()
#     print dfa.head()