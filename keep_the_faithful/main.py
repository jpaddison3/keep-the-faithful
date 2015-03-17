'''
Currently the main module, as well as storing the module
'''
import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import cross_val_score, train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from statsmodels.api import Logit
from sampled_forest import SampledForest
import utilities
import feature_engineering


def prep_data():
    '''
    Loads data from file, feature engineers and then writes to file
    '''
    d = '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/'
    dates_train = [pd.to_datetime('10/1/2005'), pd.to_datetime('10/1/2006'),
                   pd.to_datetime('10/1/2007'), pd.to_datetime('10/1/2008')]
    dfn_train = utilities.combine_load(dates_train)
    X_train, y_train, name_ids_train, dfn_train = \
        feature_engineering.model_prep(dfn_train)
    np.savetxt(d + 'X_train.csv', X_train, delimiter=', ')
    np.savetxt(d + 'y_train.csv', y_train, delimiter=', ')
    np.savetxt(d + 'name_ids_train.csv', name_ids_train, delimiter=', ')
    np.savetxt(d + 'columns_train.csv', dfn_train.columns, fmt='%s', delimiter=', ')

    dates_test = [pd.to_datetime('10/1/2009'), pd.to_datetime('10/1/2010')]
    dfn_test = utilities.combine_load(dates_test)
    X_test, y_test, name_ids_test, dfn_test = \
        feature_engineering.model_prep(dfn_test)
    np.savetxt(d + 'X_test.csv', X_test, delimiter=', ')
    np.savetxt(d + 'y_test.csv', y_test, delimiter=', ')
    np.savetxt(d + 'name_ids_test.csv', name_ids_test, delimiter=', ')
    np.savetxt(d + 'columns_test.csv', dfn_test.columns, 
               fmt='%s', delimiter=', ')

def load_prepped_data():
    '''
    Loads the pre-transformed data from file
    '''
    d = '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/'
    X_train = np.loadtxt(d + 'X_train.csv', delimiter=', ')
    y_train = np.loadtxt(
        '/Users/jpaddison/Documents/Zipfian/KeepTheFaithful/processed_data/' +
        'y_train.csv', delimiter=', ')
    name_ids_train = np.loadtxt(d + 'name_ids_train.csv', delimiter=', ')
    columns_train = np.loadtxt(d + 'columns_train.csv', 
                               dtype='str', delimiter=', ')
    X_test = np.loadtxt(d + 'X_test.csv', delimiter=', ')
    y_test = np.loadtxt(d + 'y_test.csv', delimiter=', ')
    name_ids_test = np.loadtxt(d + 'name_ids_test.csv', delimiter=', ')
    columns_test = np.loadtxt(d + 'columns_test.csv', 
                              dtype='str', delimiter=', ')

    return X_train, y_train, name_ids_train, columns_train, X_test, y_test, \
        name_ids_test, columns_test


def predict_now(today, sf):
    dfn = utilities.full_load(today)
    X_now, name_ids_now, dfn_now = \
        feature_engineering.model_prep(dfn)
    predict_list_all = sf.predict(X_now)
    return name_ids_now[predict_list_all]


def print_test_metrics(y_true, y_pred):
    print confusion_matrix(y_true, y_pred)
    print 'recall:    ', recall_score(y_true, y_pred)
    print 'precision: ', precision_score(y_true, y_pred)


if __name__ == '__main__':
    # [Prep and] load data
    prep_data()
    X_train, y_train, name_ids_train, columns_train, X_test, y_test, \
        name_ids_test, columns_test = load_prepped_data()
    print 'churn', y_train.mean()
    print 'churn test', y_test.mean()

    # Build Model
    # scaler = StandardScaler()
    # X_train = scaler.fit_transform(X_train)
    # sf = SVC(class_weight={0:1, 1:4}, C=.1)
    sf = SampledForest()
    # sf = Logit(y_train, X_train)
    # results = sf.fit()
    # print columns_train
    # print results.summary()
    sf.fit(X_train, y_train)

    sorted_args = np.argsort(sf.feature_importances_)[::-1]
    print zip(columns_train[sorted_args], sf.feature_importances_[sorted_args])
    # X_test = scaler.transform(X_test)
    print '-- train'
    print_test_metrics(y_train, sf.predict(X_train))
    print '-- test'
    print_test_metrics(y_test, sf.predict(X_test))
    
