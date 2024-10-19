from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np
import pandas as pd
from numba import njit

# Move Numba-accelerated functions outside the class
@njit
def gini(y):
    class_probs = np.bincount(y) / len(y)
    return 1 - np.sum(class_probs ** 2)

@njit
def information_gain(parent_y, left_y, right_y):
    num_left = len(left_y)
    num_right = len(right_y)
    num_total = num_left + num_right

    if num_total == 0:
        return 0

    gini_parent = gini(parent_y)
    gini_left = gini(left_y)
    gini_right = gini(right_y)

    weighted_gini = (num_left / num_total) * gini_left + (num_right / num_total) * gini_right
    return gini_parent - weighted_gini

class DTreeClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, feature_names, max_depth=None, min_gain=0.01, n_jobs=-1):
        self.feature_names = feature_names
        self.max_depth = max_depth
        self.min_gain = min_gain
        self.n_jobs = n_jobs
        self.tree = None
        self.classes_ = None

    def fit(self, X, y):
        y = np.array(y)
        self.classes_ = np.unique(y)

        if isinstance(X, pd.DataFrame):
            X = X.values

        self.tree = self._build_tree(X, y, depth=0)
        return self

    def _build_tree(self, X, y, depth):
        num_samples, num_features = X.shape
        num_labels = len(np.unique(y))

        if num_labels == 1 or depth == self.max_depth or num_samples == 0:
            return self._most_common_label(y)

        best_feature, best_split, best_gain = self._best_split(X, y)
        if best_feature is None or best_split is None or best_gain < self.min_gain:
            return self._most_common_label(y)

        left_indices, right_indices = self._split(X[:, best_feature], best_split)

        left_subtree = self._build_tree(X[left_indices, :], y[left_indices], depth + 1)
        right_subtree = self._build_tree(X[right_indices, :], y[right_indices], depth + 1)

        return {
            'feature': self.feature_names[best_feature],
            'split': best_split,
            'left': left_subtree,
            'right': right_subtree
        }

    def _best_split(self, X, y):
        best_gain = float('-inf')
        best_feature, best_split = None, None
        num_samples, num_features = X.shape

        for feature_idx in range(num_features):
            feature_values = X[:, feature_idx]
            unique_values = np.unique(feature_values)

            for threshold in unique_values:
                left_indices, right_indices = self._split(feature_values, threshold)
                if len(left_indices) == 0 or len(right_indices) == 0:
                    continue

                gain = information_gain(y, y[left_indices], y[right_indices])  # Call the Numba-accelerated function
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature_idx
                    best_split = threshold

        return best_feature, best_split, best_gain

    def _split(self, feature_column, split_value):
        if isinstance(split_value, (str, np.object_)):
            left_indices = np.where(feature_column == split_value)[0]
            right_indices = np.where(feature_column != split_value)[0]
        else:
            left_indices = np.where(feature_column < split_value)[0]
            right_indices = np.where(feature_column >= split_value)[0]
        return left_indices, right_indices

    def _most_common_label(self, y):
        return np.bincount(y).argmax()

    def predict(self, X):
        if isinstance(X, pd.DataFrame):
            X = X.values
        return np.array([self._predict_single(x, self.tree) for x in X])

    def _predict_single(self, x, tree):
        if not isinstance(tree, dict):
            return tree

        feature_idx = self.feature_names.index(tree['feature'])
        feature_value = x[feature_idx]

        if isinstance(tree['split'], (str, np.object_)):
            if feature_value == tree['split']:
                return self._predict_single(x, tree['left'])
            else:
                return self._predict_single(x, tree['right'])
        else:
            if feature_value < tree['split']:
                return self._predict_single(x, tree['left'])
            else:
                return self._predict_single(x, tree['right'])

    def get_params(self, deep=True):
        return {"feature_names": self.feature_names, "max_depth": self.max_depth, "min_gain": self.min_gain}

    def set_params(self, **params):
        for key, value in params.items():
            setattr(self, key, value)
        return self
