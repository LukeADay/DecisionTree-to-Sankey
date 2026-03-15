import sys
import os

# Add the src directory to the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from src import DecisionTree_to_Sankey


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

    def test_validation_order_non_dataframe(self):
        # isinstance check must happen before .empty so non-DataFrames raise ValueError
        import numpy as np
        with self.assertRaises(ValueError):
            DecisionTree_to_Sankey(self.clf, np.array([[1, 2], [3, 4]]))

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

    def test_no_node_merging_same_label(self):
        """
        Distinct tree nodes that produce the same label (same feature + threshold)
        must NOT be merged into a single Sankey node.
        """
        from sklearn.tree import DecisionTreeClassifier as DTC
        # Build a dataset where the tree is likely to reuse the same split feature
        # at multiple nodes.  Force max_depth so structure is predictable.
        data = pd.DataFrame({
            'F': [1, 2, 3, 4, 5, 6, 7, 8],
        })
        target = [0, 1, 0, 1, 0, 1, 0, 1]
        clf = DTC(random_state=0)
        clf.fit(data, target)

        dt_sankey = DecisionTree_to_Sankey(clf, data)
        node_data = dt_sankey._extract_tree_structure()

        # Every entry must have a unique sklearn node ID (index 0)
        node_ids = [nd[0] for nd in node_data]
        self.assertEqual(len(node_ids), len(set(node_ids)), "Duplicate sklearn node IDs in extracted structure")

        # Every Sankey label must correspond to a unique sklearn node ID
        dt_sankey.create_sankey()
        sankey_link = dt_sankey.fig.data[0].link
        # source and target indices must all be valid
        num_labels = len(dt_sankey.fig.data[0].node.label)
        for s, t in zip(sankey_link.source, sankey_link.target):
            self.assertGreaterEqual(s, 0)
            self.assertLess(s, num_labels)
            self.assertGreaterEqual(t, 0)
            self.assertLess(t, num_labels)

    def test_sample_counts_as_link_values(self):
        """
        Link values must equal the number of training samples at each child node,
        not the hardcoded constant 1.
        """
        dt_sankey = DecisionTree_to_Sankey(self.clf, self.data)
        dt_sankey.create_sankey()
        link_values = list(dt_sankey.fig.data[0].link.value)
        # All values must be positive integers
        for v in link_values:
            self.assertIsInstance(v, int)
            self.assertGreater(v, 0)
        # Total samples flowing through the root's children must equal len(data)
        # (root has exactly two children whose sample counts sum to len(data))
        self.assertEqual(sum(link_values[:2]), len(self.data))

    def test_correct_leaf_predictions_classifier(self):
        """
        Leaf labels must reflect the actual majority class at each leaf, not
        an arbitrary index into tree_.value.
        """
        dt_sankey = DecisionTree_to_Sankey(self.clf, self.data)
        node_data = dt_sankey._extract_tree_structure()
        import numpy as np
        for nd in node_data:
            node, depth, name, threshold, left, right, value_sets = nd
            if name == "Leaf":
                expected = f"Class {self.clf.classes_[np.argmax(self.clf.tree_.value[node][0])]}"
                actual = dt_sankey._outcome_at_node(node)
                self.assertEqual(actual, expected)

    def test_value_sets_narrow_correctly(self):
        """
        After a split on feature F <= threshold:
        - left child's value_sets[F] must contain only values <= threshold
        - right child's value_sets[F] must contain only values  > threshold
        """
        dt_sankey = DecisionTree_to_Sankey(self.clf, self.data)
        node_data = dt_sankey._extract_tree_structure()
        sklearn_id_to_idx = {nd[0]: i for i, nd in enumerate(node_data)}

        for nd in node_data:
            node, depth, name, threshold, left, right, value_sets = nd
            if name == "Leaf":
                continue
            left_nd = node_data[sklearn_id_to_idx[left]]
            right_nd = node_data[sklearn_id_to_idx[right]]
            for v in left_nd[6][name]:
                self.assertLessEqual(v, threshold,
                    f"Left child value {v} > threshold {threshold} for feature {name}")
            for v in right_nd[6][name]:
                self.assertGreater(v, threshold,
                    f"Right child value {v} <= threshold {threshold} for feature {name}")


if __name__ == '__main__':
    unittest.main()
