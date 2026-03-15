import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.tree import _tree
class DecisionTree_to_Sankey():
    """
    Class to visualize a trained decision tree (regression or classification) as a Plotly-based Sankey diagram.

    Parameters
    ----------
    clf : DecisionTreeClassifier or DecisionTreeRegressor
        Trained decision tree model (classifier or regressor) from scikit-learn.
    X : pd.DataFrame
        Training dataset used to grab the feature names for visualizing the tree.

    Attributes
    ----------
    clf : DecisionTreeClassifier or DecisionTreeRegressor
        The trained decision tree model.
    tree_ : Tree
        The internal tree structure of the trained model.
    feature_names : pd.Index
        Names of the features in the training data.
    is_classifier : bool
        Whether the model is a classifier.
    outcomes : array or None
        Class labels (for classifiers) or None for regressors.

    Methods
    -------
    create_sankey(title="Decision Tree Sankey Diagram")
        Generates and displays a Plotly Sankey diagram based on the decision tree.
    """


    
    def __init__(self, clf, X):
        if not hasattr(clf, 'tree_'):
            raise ValueError("The model is not a trained decision tree.")
        if not isinstance(X, pd.DataFrame):
            raise ValueError("Input data X should be a pandas DataFrame.")
        if X.empty:
            raise ValueError("Input dataset is empty.")
        self.clf = clf
        self.X = X
        self.feature_names = X.columns
        self.tree_ = clf.tree_
        # Determine if the tree is a classifier or regressor
        if hasattr(clf, 'classes_'):
            self.is_classifier = True
            self.outcomes = clf.classes_  # Class labels for classification
        else:
            self.is_classifier = False
            self.outcomes = None  # For regression, there are no class labels
    
    def _extract_tree_structure(self):
        """
        Internal function to extract tree structure.

        Returns a list of tuples:
            (sklearn_node_id, depth, name, threshold, left_child_id, right_child_id, value_sets)

        ``value_sets`` is a dict mapping each feature name to the set of unique
        training-data values that can reach this node.
        """
        # At the root every feature has its full set of unique values from X.
        initial_value_sets = {feat: set(self.X[feat].unique()) for feat in self.feature_names}

        node_info = []

        def recurse(node, depth, value_sets):
            if self.tree_.feature[node] != _tree.TREE_UNDEFINED:
                # Not a leaf node
                name = self.feature_names[self.tree_.feature[node]]
                threshold = self.tree_.threshold[node]
                left_child = self.tree_.children_left[node]
                right_child = self.tree_.children_right[node]
                node_info.append((node, depth, name, threshold, left_child, right_child, value_sets))

                # Left (True) child: feature values <= threshold
                left_value_sets = dict(value_sets)
                left_value_sets[name] = {v for v in value_sets[name] if v <= threshold}
                recurse(left_child, depth + 1, left_value_sets)

                # Right (False) child: feature values > threshold
                right_value_sets = dict(value_sets)
                right_value_sets[name] = {v for v in value_sets[name] if v > threshold}
                recurse(right_child, depth + 1, right_value_sets)
            else:
                # Leaf node
                node_info.append((node, depth, "Leaf", None, None, None, value_sets))

        recurse(0, 0, initial_value_sets)
        return node_info
    
    def create_sankey(self, title="Decision Tree Sankey Diagram"):
        """
        Creates a Sankey diagram showing the structure of the decision tree.

        Parameters
        ----------
        title : str, optional
            The title of the Sankey diagram. Default is "Decision Tree Sankey Diagram".
        """

        # Extract the tree structure
        node_data = self._extract_tree_structure()

        # Build a mapping from sklearn node ID → index in node_data
        sklearn_id_to_idx = {nd[0]: i for i, nd in enumerate(node_data)}

        # Prepare the data for a Sankey diagram
        labels = []
        source = []
        target = []
        values = []
        hover_text = []  # To store custom hover text for the branches

        # Keyed by sklearn node ID (int) so distinct nodes never merge
        node_id = {}
        counter = 0

        for nd in node_data:
            node, depth, name, threshold, left, right, value_sets = nd

            if name != "Leaf":
                node_name = f"{name} <= {threshold:.2f}"
            else:
                # Leaf nodes: show predicted outcome (either class or value)
                outcome = self._outcome_at_node(node)
                node_name = f"Leaf: {outcome}"

            if node not in node_id:
                node_id[node] = counter
                labels.append(node_name)
                counter += 1

            # Left branch (True condition)
            if left is not None and name != "Leaf":
                left_nd = node_data[sklearn_id_to_idx[left]]
                if left_nd[2] != "Leaf":
                    left_name = f"{left_nd[2]} <= {left_nd[3]:.2f}"
                else:
                    left_name = f"Leaf: {self._outcome_at_node(left)}"
                if left not in node_id:
                    node_id[left] = counter
                    labels.append(left_name)
                    counter += 1
                source.append(node_id[node])
                target.append(node_id[left])
                values.append(int(self.tree_.n_node_samples[left]))
                left_vals = sorted(left_nd[6][name])
                hover_text.append(
                    f"{name} <= {threshold:.2f} (True)<br>{name}: {left_vals}"
                )

            # Right branch (False condition)
            if right is not None and name != "Leaf":
                right_nd = node_data[sklearn_id_to_idx[right]]
                if right_nd[2] != "Leaf":
                    right_name = f"{right_nd[2]} <= {right_nd[3]:.2f}"
                else:
                    right_name = f"Leaf: {self._outcome_at_node(right)}"
                if right not in node_id:
                    node_id[right] = counter
                    labels.append(right_name)
                    counter += 1
                source.append(node_id[node])
                target.append(node_id[right])
                values.append(int(self.tree_.n_node_samples[right]))
                right_vals = sorted(right_nd[6][name])
                hover_text.append(
                    f"{name} > {threshold:.2f} (False)<br>{name}: {right_vals}"
                )

        # Create the Sankey diagram
        fig = go.Figure(go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels
            ),
            link=dict(
                source=source,
                target=target,
                value=values,
                customdata=hover_text,  # Add custom hover text
                hovertemplate='%{customdata}<extra></extra>'  # Use custom hover text
            )
        ))
        fig.update_layout(title_text=title, font_size=10)
        self.fig = fig
        fig.show()
    def _outcome_at_node(self, node):
        """
        This is an internal method and should not be called directly by users.
        Returns the predicted outcome at a leaf node.
        For classifiers, this returns the class with the highest probability.
        For regressors, this returns the predicted value.
        """
        if self.is_classifier:
            return f"Class {self.outcomes[np.argmax(self.tree_.value[node][0])]}"
        else:
            return f"Value {np.mean(self.tree_.value[node][0]):.2f}"