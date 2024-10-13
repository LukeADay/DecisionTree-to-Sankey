import sys
import os

# Add the src directory to the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


import unittest
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from src.DecisionTree_To_Sankey import DecisionTree_to_Sankey

class TestDecisionTreeToSankey(unittest.TestCase):
    def setUp(self):
        # Set up a simple decision tree and dataset to use in the tests
        self.clf = DecisionTreeClassifier()
        self.data = pd.DataFrame({
            'Feature1': [1, 2, 3, 4],
            'Feature2': [5, 6, 7, 8]
        })
        self.target = [0, 1, 0, 1]
        self.clf.fit(self.data, self.target)
    
    def test_create_sankey(self):
        # Test if the sankey diagram can be created without errors
        dt_sankey = DecisionTree_to_Sankey(self.clf, self.data)
        self.assertIsNotNone(dt_sankey)  # Ensure that the object is created successfully
    
    def test_create_sankey_output(self):
        # Test if the create_sankey method generates a figure without errors
        dt_sankey = DecisionTree_to_Sankey(self.clf, self.data)
        dt_sankey.create_sankey()
        self.assertIsNotNone(dt_sankey.fig)  # Ensure that a figure is created
    
    def test_sankey_with_empty_data(self):
        # Test handling of an empty dataset
        empty_data = pd.DataFrame({'Feature1': [], 'Feature2': []})
        with self.assertRaises(ValueError):  # Ensure that an error is raised for invalid input
            dt_sankey = DecisionTree_to_Sankey(self.clf, empty_data)

    def test_regression_tree(self):
        # Set up a regression tree
        from sklearn.tree import DecisionTreeRegressor
        reg_clf = DecisionTreeRegressor()
        data = pd.DataFrame({
            'Feature1': [1, 2, 3, 4],
            'Feature2': [5, 6, 7, 8]
        })
        target = [10, 15, 10, 15]
        reg_clf.fit(data, target)

        # Create Sankey diagram for regression tree
        dt_sankey = DecisionTree_to_Sankey(reg_clf, data)
        dt_sankey.create_sankey()
        self.assertIsNotNone(dt_sankey.fig)  # Ensure the Sankey figure is created


if __name__ == '__main__':
    unittest.main()
