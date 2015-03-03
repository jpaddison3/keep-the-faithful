import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.metrics import precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score

# --------------- Load Data ---------------------------------- #
# attendance dataframe
dfa = pd.read_csv(
    '/Users/jpaddison/Documents/Zipfian/ProjectData/Att09-10.csv')
# user info dataframe
dfn = pd.read_csv('/Users/jpaddison/Documents/Zipfian/ProjectData/NANames.csv')
# address dataframe
dfadd = pd.read_csv(
    '/Users/jpaddison/Documents/Zipfian/ProjectData/NAAddresses.csv')

# ------------- Select, combine and clean user info ------------------#
# select for year
explore_year = pd.to_datetime('2010').year
dfa['Date'] = pd.to_datetime(dfa['Date'])
dfa = dfa[dfa['Date'].apply(lambda x: x.year) == explore_year]
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

# ----------- Feature engineering ------------- #
today = pd.to_datetime('10/1/2010')
recent_sundays = (dfa['Organization'] == 'Sunday Worship') & \
                 (pd.to_datetime(dfa['Date']) >=
                  today - np.timedelta64(2, 'M'))
recent_attendance_numbers = dfa[recent_sundays]\
    .groupby(['NameID'])['Date'].nunique()
recent_users = recent_attendance_numbers[recent_attendance_numbers >= 2].index

year_attendance_numbers = dfa[dfa['Organization'] == 'Sunday Worship']\
    .groupby(['NameID'])['Date'].nunique()
year_users = year_attendance_numbers[year_attendance_numbers >= 2].index

solid_users = set(recent_users) & set(year_users)

# solid user info
print len(solid_users)
su_info = dfn[dfn['NameCounter'].isin(solid_users)]
print len(su_info)  # WHERE'D HE GO ###################################
# solid user attendance
su_att = dfa[dfa['NameID'].isin(solid_users)]
su_info = su_info.set_index('NameCounter')

present_users = su_att[
    (su_att['Date'] == '9/26/2010') &
    (dfa['Organization'] == 'Sunday Worship')]['NameID'].values
su_info['t-1'] = 0
su_info['t-1'] = pd.Series(su_info.index.isin(present_users).astype('int'),
                           index=su_info.index)

present_users = su_att[
    (su_att['Date'] == '9/19/2010') &
    (dfa['Organization'] == 'Sunday Worship')]['NameID'].values
su_info['t-2'] = 0
su_info['t-2'] = pd.Series(su_info.index.isin(present_users).astype('int'),
                           index=su_info.index)

present_users = su_att[
    (su_att['Date'] == '9/12/2010') &
    (dfa['Organization'] == 'Sunday Worship')]['NameID'].values
su_info['t-3'] = 0
su_info['t-3'] = pd.Series(su_info.index.isin(present_users).astype('int'),
                           index=su_info.index)

present_users = su_att[
    (su_att['Date'] == '9/5/2010') &
    (dfa['Organization'] == 'Sunday Worship')]['NameID'].values
su_info['t-4'] = 0
su_info['t-4'] = pd.Series(su_info.index.isin(present_users).astype('int'),
                           index=su_info.index)

present_users = su_att[
    (su_att['Date'] >= pd.to_datetime('10/1/2010')) &
    (su_att['Date'] <= pd.to_datetime('12/12/2010')) &
    (dfa['Organization'] == 'Sunday Worship')]['NameID'].values
su_info['churn'] = 0
su_info['churn'] = pd.Series((~su_info.index.isin(present_users))
                             .astype('int'), index=su_info.index)
print su_info['churn'].mean()

# ------------- Ready the features for model ------------ #
su_info = su_info.drop(['City'], axis=1)
su_info['WhenSetup'] = pd.to_datetime(su_info['WhenSetup'])\
    .apply(lambda x: x.year)
su_info = pd.get_dummies(su_info)
y = su_info.pop('churn').values
X = su_info.values

# ------------------------- MODEL -------------------------- #
rf = RandomForestClassifier()

print cross_val_score(rf, X, y, scoring='precision', cv=2)

rf.fit(X, y)
print precision_score(y, rf.predict(X))
print su_info.columns
print rf.feature_importances_

# There seems to be a problem with the imbalanced class distributon
