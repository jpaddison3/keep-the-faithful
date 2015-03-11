import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append(
    '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/keep_the_faithful')
import utilities
import feature_engineering


def plot_age(dfn, df_churned):
    ages = df_churned[df_churned['Age'] < 150]['Age'].values
    plt.hist(ages, bins=20)

def plot_church_age(dfn, df_churned):
    plt.hist(df_churned['YearsInChurch'].values)

def plot_time_since_attending(dfn, df_churned):
    missed_time_all = np.ones(len(dfn)) - 1
    for w in range(8, 0, -1):
        att = dfn['t-' + str(w)].values
        missed_time_all[att != 0] = w
    missed_time_churn = np.ones(len(df_churned)) - 1
    for w in range(8, 0, -1):
        att = df_churned['t-' + str(w)].values
        missed_time_churn[att != 0] = w
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].hist(missed_time_all, bins=7)
    axarr[0].set_title('Churn by time since attending service')
    axarr[1].hist(missed_time_churn, bins=7)

if __name__ == '__main__':
    dates = [pd.to_datetime('10/1/2005'), pd.to_datetime('10/1/2006')]
    dfn = utilities.combine_load(dates)

    df_churned = dfn[dfn['churn'] == 1]

    plot_time_since_attending(dfn, df_churned)
    plt.show()