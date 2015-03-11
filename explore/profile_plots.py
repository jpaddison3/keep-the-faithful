import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append(
    '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/keep_the_faithful')
import utilities
import feature_engineering


def prof_plot(df):
    f, ax = plt.subplots(4, 4, sharex='col', sharey='row')
    attendance_cols = ['t-' + str(i) for i in xrange(8, 0, -1)]
    for i in xrange(len(df)):
        color = 'r' if df.iloc[i]['churn'] else 'b'
        ax[i/4][i%4].plot(range(8), df.iloc[i][attendance_cols], 
            color=color)
    ax[0][0].set_title('title')

if __name__ == '__main__':
    today = pd.to_datetime('10/1/2008')
    dfn = utilities.full_load(today)
    dfn = dfn.iloc[:16]
    prof_plot(dfn)
    plt.show()
