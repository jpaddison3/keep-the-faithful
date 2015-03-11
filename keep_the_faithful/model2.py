'''
Currently the main module, as well as storing the module
'''
import pandas as pd
import numpy as np
from sklearn.metrics import precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score, train_test_split
from sklearn.metrics import confusion_matrix
import sys
sys.path.append(
    '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/keep_the_faithful')
import utilities
import feature_engineering


def prep_data():
    '''
    Loads data from file, feature engineers and then writes to file
    '''
    dates_train = [pd.to_datetime('10/1/2005'), pd.to_datetime('10/1/2006'),
                   pd.to_datetime('10/1/2007'), pd.to_datetime('10/1/2008')]
    dfn_train = utilities.combine_load(dates_train)
    X_train, y_train, name_ids_train, dfn_train = \
        feature_engineering.model_prep(dfn_train)
    np.savetxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'X_train.csv', X_train, delimiter=', ')
    np.savetxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'y_train.csv', y_train, delimiter=', ')
    np.savetxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'name_ids_train.csv', name_ids_train, delimiter=', ')
    np.savetxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'columns_train.csv', dfn_train.columns, fmt='%s', delimiter=', ')

    dates_test = [pd.to_datetime('10/1/2009'), pd.to_datetime('10/1/2010')]
    dfn_test = utilities.combine_load(dates_test)
    X_test, y_test, name_ids_test, dfn_test = \
        feature_engineering.model_prep(dfn_test)
    np.savetxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'X_test.csv', X_test, delimiter=', ')
    np.savetxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'y_test.csv', y_test, delimiter=', ')
    np.savetxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'name_ids_test.csv', name_ids_test, delimiter=', ')
    np.savetxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'columns_test.csv', dfn_test.columns, fmt='%s', delimiter=', ')

def load_prepped_data():
    '''
    Loads the pre-transformed data from file
    '''
    X_train = np.loadtxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'X_train.csv', delimiter=', ')
    y_train = np.loadtxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'y_train.csv', delimiter=', ')
    name_ids_train = np.loadtxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'name_ids_train.csv', delimiter=', ')
    columns_train = np.loadtxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'columns_train.csv', dtype='str', delimiter=', ')
    X_test = np.loadtxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'X_test.csv', delimiter=', ')
    y_test = np.loadtxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'y_test.csv', delimiter=', ')
    name_ids_test = np.loadtxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'name_ids_test.csv', delimiter=', ')
    columns_test = np.loadtxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'columns_test.csv', dtype='str', delimiter=', ')

    return X_train, y_train, name_ids_train, columns_train, X_test, y_test, \
        name_ids_test, columns_test


class sampled_forests(object):
    '''
    Downsamples the majority class and upsamples the minority, then models 
    using randomm forest.  This is repeated and each forest gets a vote.
    '''
    def __init__(self):
        pass

    def resample(self, X, y):
        '''
        Downsamples the majority class and upsamples the minority
        '''
        majority_ndxs = np.arange(len(y))[y == 0]
        delete_rows = np.random.choice(majority_ndxs,
                                       int(len(majority_ndxs) * .5))
        X = np.delete(X, delete_rows, 0)
        y = np.delete(y, delete_rows)
        minority_ndxs = np.arange(len(y))[y == 1]
        add_rows = np.random.choice(minority_ndxs, int(len(minority_ndxs) * .5))
        X = np.vstack([X, X[add_rows]])
        y = np.concatenate([y, y[add_rows]])
        return X, y

    def fit(self, X, y):
        '''
        Trains random forest models
        '''
        self.models = []
        for i in xrange(20):
            X_i, y_i = self.resample(X, y)
            rf = RandomForestClassifier(n_estimators=80, min_samples_split=6)
            rf.fit(X_i, y_i, sample_weight=y_i/y_i.mean()+1)
            self.models.append(rf)

    def predict(self, X):
        '''
        Predicts labels for each row in X
        '''
        votes_mat = np.zeros((len(self.models), len(X)))
        for i, model in enumerate(self.models):
            votes_mat[i] = model.predict(X)
        return votes_mat.mean(0) > .3

if __name__ == '__main__':
    # [Prep and] load data
    # prep_data()
    X_train, y_train, name_ids_train, columns_train, X_test, y_test, \
        name_ids_test, columns_test = load_prepped_data()

    # Build Model
    rf = RandomForestClassifier(n_estimators=80)
    rf = sampled_forests()
    rf.fit(X_train, y_train)

    print precision_score(y_train, rf.predict(X_train))
    print precision_score(y_test, rf.predict(X_test))
    print confusion_matrix(y_train, rf.predict(X_train))
    print confusion_matrix(y_test, rf.predict(X_test))
