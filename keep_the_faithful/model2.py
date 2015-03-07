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

dfn, dfa, dfadd, dfr = utilities.load_data()
print '.'
dfn, dfa = utilities.clean_data(dfn, dfa, dfadd)
print '.'
dfn, dfa = feature_engineering.select_active(dfn, dfa)
print '.'
dfn = feature_engineering.add_churn(dfn, dfa)
print '.'
dfn = feature_engineering.add_recent_attendance(dfn, dfa)
print '.'
dfn = feature_engineering.add_small_groups(dfn, dfa)
print '.'
dfn = feature_engineering.add_family(dfn, dfr)
print '.'
X, y, name_ids, dfn = feature_engineering.model_prep(dfn)

rf = RandomForestClassifier()

print cross_val_score(rf, X, y, scoring='precision', cv=2)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

rf.fit(X_train, y_train)
print precision_score(y_train, rf.predict(X_train))
print precision_score(y_test, rf.predict(X_test))
print dfn.columns
print rf.feature_importances_
print confusion_matrix(y_train, rf.predict(X_train))
print confusion_matrix(y_test, rf.predict(X_test))