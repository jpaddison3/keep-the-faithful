import pandas as pd
import numpy as np
import sys
sys.path.append(
    '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/keep_the_faithful')
import utilities
import feature_engineering

dates = [pd.to_datetime('10/1/2005'), pd.to_datetime('10/1/2006'),
         pd.to_datetime('10/1/2007'), pd.to_datetime('10/1/2008'),
         pd.to_datetime('10/1/2009'), pd.to_datetime('10/1/2010')]
dfn = utilities.combine_load(dates)

# Do this first for speed
dfn['RecentAttendance'] = dfn['t-1'] + dfn['t-2'] + dfn['t-3'] + dfn['t-4']

df_churned = dfn[dfn['churn'] == 1]
df_stayed = dfn[dfn['churn'] == 0]

# ---------------------- Walk through features ----------------- #
#    --- Birth year was nan
print '-- Birth year was nan --'
print 'all', np.mean(dfn['BirthYear'] == 1800)
print 'churned users', np.mean(df_churned['BirthYear'] == 1800)
print 'staying users', np.mean(df_stayed['BirthYear'] == 1800)
#    --- Average age
print '-- Average age --'
print 'all', dfn[dfn['BirthYear'] != 1800]['Age'].mean()
print 'churned', df_churned[df_churned['BirthYear'] != 1800]['Age'].mean()
print 'staying', df_stayed[df_stayed['BirthYear'] != 1800]['Age'].mean()
#    --- Gender
print '-- Gender --'
print '  all  '
print 'Male', np.mean(dfn['Gender'] == 'M')
print 'Female', np.mean(dfn['Gender'] == 'F')
print 'Not specified', np.mean(dfn['Gender'] == 'N')
print '  churned  '
print 'Male', np.mean(df_churned['Gender'] == 'M')
print 'Female', np.mean(df_churned['Gender'] == 'F')
print 'Not specified', np.mean(df_churned['Gender'] == 'N')
print '  staying  '
print 'Male', np.mean(df_stayed['Gender'] == 'M')
print 'Female', np.mean(df_stayed['Gender'] == 'F')
print 'Not specified', np.mean(df_stayed['Gender'] == 'N')
#   --- Years In Church
print '-- Years In Church --'
print 'all', dfn['YearsInChurch'].mean()
print 'churned users', df_churned['YearsInChurch'].mean()
print 'staying users', df_stayed['YearsInChurch'].mean()
#   --- Recent Attendance
print '-- Recent Attendance --'
print 'all', dfn['RecentAttendance'].mean()
print 'churned users', df_churned['RecentAttendance'].mean()
print 'staying users', df_stayed['RecentAttendance'].mean()
#   -- Small Groups
print '-- In a Small Group --'
print 'all', dfn['InSG'].mean()
print 'churned', df_churned['InSG'].mean()
print 'staying', df_stayed['InSG'].mean()
print '-- Small Group Attendance --'
print 'all', dfn['SGPercentage'].mean()
print 'churned', df_churned['SGPercentage'].mean()
print 'staying', df_stayed['SGPercentage'].mean()
#   --- Family Size
print '-- Family Size --'
print 'all', dfn['Family'].mean()
print 'churned', df_churned['Family'].mean()
print 'staying', df_stayed['Family'].mean()
