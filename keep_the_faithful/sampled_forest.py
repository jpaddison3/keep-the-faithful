import numpy as np
from sklearn.ensemble import RandomForestClassifier


class SampledForest(object):
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
        num_forests = 20
        self.models = []
        self.feature_importances_ = np.zeros(X.shape[1])
        for i in xrange(num_forests):
            X_i, y_i = self.resample(X, y)
            rf = RandomForestClassifier(n_estimators=80, min_samples_split=6)
            # rf = SVC(class_weight='auto')
            rf.fit(X_i, y_i, sample_weight=y_i/y_i.mean()+1)
            self.models.append(rf)
            self.feature_importances_ += rf.feature_importances_
        self.feature_importances_ /= num_forests

    def predict(self, X):
        '''
        Predicts labels for each row in X
        '''
        votes_mat = np.zeros((len(self.models), len(X)))
        for i, model in enumerate(self.models):
            votes_mat[i] = model.predict(X)
        return votes_mat.mean(0) > .3
