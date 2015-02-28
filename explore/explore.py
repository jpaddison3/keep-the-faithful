'''
JP Addison

Beginning exploration
'''
import numpy as np
import pandas as pd

explore_year = '2010'
# attendance dataframe
dfa = pd.read_csv('/Users/jpaddison/Documents/Zipfian/ProjectData/Att09-10.csv')
dfa = dfa[dfa['Date'].str[-4:]==explore_year]
# people's relationship info
dfr = pd.read_csv('/Users/jpaddison/Documents/Zipfian/ProjectData/NARelations.csv')

# ------- Find attender information ----------- #
attendance_numbers = dfa[dfa['Organization']=='Sunday Worship']\
                     .groupby(['NameID'])['Date'].count()
attendance_numbers.sort(ascending=False) # why the heck is this inplace

# print 'attendance'
# print attendance_numbers
# # Person who's attended 45 times, manually selected
# some_person = 22969
# # some_person doesn't have an relationships entered
# print 'some_person\'s relationships'
# print dfr[(dfr['NameCounterHigh'] == some_person) | \
#           (dfr['NameCounterLow'] == some_person)]
# # some_person also has no small groups
# print 'some_person\'s attendance'
# print dfa[dfa['NameID']==some_person]

# ------- Find percentage of returning users in small groups ------- #
returning_users = attendance_numbers[attendance_numbers >= 2].index

# attendace dataframe for returning users
dfar = dfa[dfa['NameID'].isin(returning_users)]

print 'percentage involved in a small group:'
print (dfar.groupby('NameID')['Organization'].unique().apply(len) > 1).mean() \
    * 100