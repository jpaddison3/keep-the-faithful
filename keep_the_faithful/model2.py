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

# Load Data
dates_train = [pd.to_datetime('10/1/2005'), pd.to_datetime('10/1/2006'),
               pd.to_datetime('10/1/2007'), pd.to_datetime('10/1/2008')]
dfn_train = utilities.combine_load(dates_train)
X_train, y_train, name_ids_train, dfn_train = \
    feature_engineering.model_prep(dfn_train)

dates_test = pd.to_datetime('10/1/2009'), pd.to_datetime('10/1/2010')
dfn_test = utilities.combine_load(dates_test)
X_test, y_test, name_ids_test, dfn_test = \
    feature_engineering.model_prep(dfn_test)

# Build Model
rf = RandomForestClassifier(n_estimators=80)
rf.fit(X_train, y_train)

print precision_score(y_train, rf.predict(X_train))
print precision_score(y_test, rf.predict(X_test))
sorted_args = np.argsort(rf.feature_importances_)[::-1]
print zip(dfn_train.columns[sorted_args], rf.feature_importances_[sorted_args])
print confusion_matrix(y_train, rf.predict(X_train))
print confusion_matrix(y_test, rf.predict(X_test))
