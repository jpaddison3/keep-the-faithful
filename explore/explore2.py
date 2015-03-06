'''
JP Addison

Beginning exploration

Unpolished
'''
import pandas as pd
import numpy as np
from collections import defaultdict

explore_year = '2010'

# user info dataframe
dfn = pd.read_csv('/Users/jpaddison/Documents/Zipfian/ProjectData/NANames.csv')
dfn = dfn.drop('SearchID', axis=1)
dfn_all = dfn.copy()
# attendance dataframe
dfa = pd.read_csv('/Users/jpaddison/Documents/Zipfian/ProjectData/Att09-10.csv')
dfa = dfa[dfa['Date'].str[-4:]==explore_year]
# Relationship datafram
dfr = pd.read_csv('/Users/jpaddison/Documents/Zipfian/ProjectData/NARelations.csv')

attendance_numbers = dfa[dfa['Organization']=='Sunday Worship']\
                     .groupby(['NameID'])['Date'].count()
returning_users = attendance_numbers[attendance_numbers >= 2].index
dfn = dfn[dfn['NameCounter'].isin(returning_users)]

useful_cols = ['BirthYear', 'Gender', 'MainAddress', 'NameCounter', 'FamNu',
               'UnitNu', 'WhenSetup']
dfn = dfn[useful_cols]
dfn = dfn.set_index('NameCounter')
dfn_all = dfn_all.set_index('NameCounter')

# print dfn.sort('FamNu')[['FamNu', 'NameCounter', 'UnitNu']]

relationship_dict = {
3:   'Grandchild',
4:   'Grandparent',
5:   'Employee',
6:   'Employer',
7:   'Grandson',
8:   'Niece',
9:   'Parent/Child',
10:  'grandparent/grandchild',
11:  'sister',
12:  'brother',
13:  'Nephew',
14:  'Divorced parent/child',
15:  'Daughter-in-law',
16:  'Non-church spouse',
17:  'Godchild',
18:  'brother-in-law',
19:  'Unclie',
20:  'Great Grandparent/Child',
21:  'Aunt',
22:  'Child',
23:  'Daughter',
24:  'son',
25:  'sister-in-law',
26:  'sibling',
27:  'Unknown',
28:  'Doctor/LAUMC CC Child',
29:  'Cousin',
30:  'In-Law',
31:  'Spouse',
32:  'other',
33:  'bushek, ann',
34:  'DECEASED SPOUSE',
35:  'Non-custodial Parent',
36:  'Former Spouse',
37:  'Aupair',
38:  'DECEASED PARENT',
39:  'DECEASED GRANDCHILD',
40:  'DECEASED CHILD',
}

def find_fam(name_id, dfn, dfr):
    fam_id = dfn.ix[name_id]['FamNu']
    fam_member_ids = dfn[dfn['FamNu'] == fam_id].index
    family_dict = defaultdict(list)
    if (dfn.ix[name_id]['UnitNu'] == 0) or (dfn.ix[name_id]['UnitNu'] == 1):
        for member_id in fam_member_ids:
            if member_id != name_id:
                if (dfn.ix[member_id]['UnitNu'] == 0) or \
                   (dfn.ix[member_id]['UnitNu'] == 1):
                    family_dict['spouse'].append(member_id)
                elif dfn.ix[member_id]['UnitNu'] == 2:
                    family_dict['children'].append(member_id)
                else:
                    family_dict['other_immediate'].append(member_id)
    elif dfn.ix[name_id]['UnitNu'] == 2:
        for member_id in fam_member_ids:
            if member_id != name_id:
                if (dfn.ix[member_id]['UnitNu'] == 0) or \
                   (dfn.ix[member_id]['UnitNu'] == 1):
                   family_dict['parent'].append(member_id)
                elif dfn.ix[member_id]['UnitNu'] == 2:
                    family_dict['sibling'].append(member_id)
                else:
                    family_dict['other_immediate'].append(member_id)
    else:
        for member_id in fam_member_ids:
            if member_id != name_id:
                family_dict['other_immediate'].append(member_id)
    relatives = dfr[(dfr['NameCounterHigh'] == name_id) | \
          (dfr['NameCounterLow'] == name_id)][['NameCounterLow', 
          'NameCounterHigh']]
    relatives_low = relatives['NameCounterLow']
    relatives_low = relatives_low[relatives_low != name_id]
    for relative_id in relatives_low:
        family_dict['extended_relatives'].append(relative_id)
    relatives_high = relatives['NameCounterHigh']
    relatives_high = relatives_high[relatives_high != name_id]
    for relative_id in relatives_high:
        family_dict['extended_relatives'].append(relative_id)
    return family_dict

# fam = find_fam(3706, dfn_all, dfr)
# print fam
# print 
# print
fam = find_fam(33099, dfn, dfr)
print fam

# # ---------------- Find family info -------------- #
# fam_sizes = []
# family_existances = []
# for name_id in dfn.index:
#     fam = find_fam(name_id, dfn, dfr)
#     if len(fam) > 0:
#         fam_sizes.append(sum([len(lst) for lst in fam.values()]))
#     family_existances.append(len(fam) > 0)
# print np.mean(fam_sizes)
# print np.mean(family_existances)

# ---------------- Churn pictures -------------- #
# address dataframe
dfadd = pd.read_csv(
    '/Users/jpaddison/Documents/Zipfian/ProjectData/NAAddresses.csv')
# select for year
explore_year = pd.to_datetime('2010').year
dfa['Date'] = pd.to_datetime(dfa['Date'])
dfa = dfa[dfa['Date'].apply(lambda x: x.year) == explore_year]
# use interesting columns
useful_cols = ['BirthYear', 'Gender', 'MainAddress',
               'WhenSetup']
dfn = dfn[useful_cols]
# merge addresses with info
dfn = dfn.rename(columns={'MainAddress': 'AddressCounter'})
dfadd = dfadd[['City', 'AddressCounter']]
dfn = pd.merge(dfn, dfadd, on='AddressCounter')
dfn = dfn.drop('AddressCounter', axis=1)
# fill nans with ridiculous things
dfn = dfn.fillna({'BirthYear': 1800, 'Gender': 'N', 'City': 'NA Land'})

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
solid_users_arr = np.array(list(solid_users))
su_info = dfn[np.in1d(dfn.index, solid_users_arr)]
# Some users are not in dfn, which is, hmm, bad
lonelies = solid_users_arr[~np.in1d(solid_users_arr, su_info.index)]
for l in lonelies:
    print l in dfn.index
    print l in dfa['NameID'].values

# solid user attendance
su_att = dfa[dfa['NameID'].isin(solid_users)]

present_users = su_att[
    (su_att['Date'] >= pd.to_datetime('10/1/2010')) &
    (su_att['Date'] <= pd.to_datetime('12/12/2010')) &
    (dfa['Organization'] == 'Sunday Worship')]['NameID'].values

su_info['churn'] = 0
su_info['churn'] = pd.Series((~su_info.index.isin(present_users))
                             .astype('int'), index=su_info.index)

churned_info = su_info[su_info['churn'] == 1]
print len(churned_info)