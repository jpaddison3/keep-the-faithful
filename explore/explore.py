'''
JP Addison

Beginning exploration
'''
import pandas as pd
import numpy as np

explore_year = '2010'

# ---------- Load from file ----------- #
# attendance dataframe
dfa = pd.read_csv('/Users/jpaddison/Documents/Zipfian/ProjectData/Att09-10.csv')
dfa = dfa[dfa['Date'].str[-4:]==explore_year]
# people info
dfn = pd.read_csv('/Users/jpaddison/Documents/Zipfian/ProjectData/NANames.csv')
# people's relationship info
dfr = pd.read_csv('/Users/jpaddison/Documents/Zipfian/ProjectData/NARelations.csv')

# ------- Sort attenders and print info  ----------- #
attendance_numbers = dfa[dfa['Organization']=='Sunday Worship']\
                     .groupby(['NameID'])['Date'].count()
attendance_numbers.sort(ascending=False) # why the heck is this inplace

print 'attendance'
print attendance_numbers
# Person who's attended 45 times, manually selected
some_person = 22969
# some_person doesn't have an relationships entered
print 'some_person\'s relationships'
print dfr[(dfr['NameCounterHigh'] == some_person) | \
          (dfr['NameCounterLow'] == some_person)]
# some_person also has no small groups
print 'some_person\'s attendance'
print dfa[dfa['NameID'] == some_person]
some_person_family = dfn[dfn['NameCounter'] == some_person]['FamNu'].values[0]
print 'famnu', some_person_family
print dfn[dfn['FamNu'] == some_person_family]
# only one person in family - o_o Jesus, he's a hundred years old

# ------- Find percentage of returning users in small groups ------- #
returning_users = attendance_numbers[attendance_numbers >= 2].index

# attendace dataframe for returning users
dfar = dfa[dfa['NameID'].isin(returning_users)]

# print 'percentage involved in a small group:'
# print (dfar.groupby('NameID')['Organization'].unique().apply(len) > 1).mean() \
#     * 100

# ------- Find demographic info ----------- #
dfn = dfn[dfn['NameCounter'].isin(returning_users)]

# -- Confirm dataframe contains all attenders
print 'should be equal:', len(returning_users), len(dfn)
# thank god that worked

print 'masculine:', np.mean(dfn['Gender'] == 'M') * 100
print 'feminine:', np.mean(dfn['Gender'] == 'F') * 100
print 'percent of people who don\'t get along with the gender binary:', \
    np.mean((dfn['Gender'] != 'M') & (dfn['Gender'] != 'F').values) * 100

dfn.info()

birth_years = dfn[dfn['BirthYear'].notnull()]['BirthYear'].values
birth_years = birth_years[birth_years > 1875]
# Run plot_hist.py for histogram, but the birth years look good except for the
# ones around 1800

print 'percent in a family', \
    (1 - len(dfn['FamNu'].unique())/float(len(dfn))) * 100

# ------ Small group data ------- #
print dfa.groupby('Organization')['NameID'].count()