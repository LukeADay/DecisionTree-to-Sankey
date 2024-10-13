import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.tree import _tree

class DecisionTree_to_Sankey():
    """
    Class to visualize a trained decision tree (regression or classification) as a Plotly-based Sankey diagram.

    Inputs:
        - clf : Trained decision tree (classifier or regressor)
        - X : Training set (DataFrame) used to grab the feature names

    Outputs:
        - A Plotly Sankey diagram visualizing the tree's structure and predictions.
    """
    
    def __init__(self, clf, X):
        if not hasattr(clf, 'tree_'):
            raise ValueError("The model is not a trained decision tree.")
        if X.empty:
            raise ValueError("Input dataset is empty.")
        if not isinstance(X, pd.DataFrame):
            raise ValueError("Input data X should be a pandas DataFrame.")

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
    
    def extract_tree_structure(self):
        """
        Internal function to extract tree structure.
        """
        node_info = []

        def recurse(node, depth):
            if self.tree_.feature[node] != _tree.TREE_UNDEFINED:
                # Not a leaf node
                name = self.feature_names[self.tree_.feature[node]]
                threshold = self.tree_.threshold[node]
                node_info.append((depth, name, threshold, self.tree_.children_left[node], self.tree_.children_right[node]))
                recurse(self.tree_.children_left[node], depth + 1)
                recurse(self.tree_.children_right[node], depth + 1)
            else:
                # Leaf node
                node_info.append((depth, "Leaf", None, None, None))
        
        recurse(0, 0)
        return node_info
    
    def create_sankey(self, title="Decision Tree Sankey Diagram"):
        """
        Creates a Plotly-based Sankey diagram showing the structure of the decision tree.
        
        Inputs:
            - (Optional) title : The title of the Sankey diagram.
        """
        # Extract the tree structure
        node_data = self.extract_tree_structure()

        # Prepare the data for a Sankey diagram
        labels = []
        source = []
        target = []
        values = []
        hover_text = []  # To store custom hover text for the branches

        node_id = {}
        counter = 0

        for idx, (depth, name, threshold, left, right) in enumerate(node_data):
            if name != "Leaf":
                node_name = f"{name} <= {threshold:.2f}"
            else:
                # Leaf nodes: show predicted outcome (either class or value)
                if self.is_classifier:
                    outcome = f"Class {self.outcomes[np.argmax(self.tree_.value[idx][0])]}"
                else:
                    # For regression, show predicted continuous value
                    outcome = f"Value {np.mean(self.tree_.value[idx][0]):.2f}"
                node_name = f"Leaf: {outcome}"

            if node_name not in node_id:
                node_id[node_name] = counter
                labels.append(node_name)
                counter += 1

            # Left branch (True condition)
            if left is not None and name != "Leaf":
                left_name = f"{node_data[left][1]} <= {node_data[left][2]:.2f}" if node_data[left][1] != "Leaf" else f"Leaf: {self.outcome_at_node(left)}"
                if left_name not in node_id:
                    node_id[left_name] = counter
                    labels.append(left_name)
                    counter += 1
                source.append(node_id[node_name])
                target.append(node_id[left_name])
                values.append(1)
                hover_text.append(f"{name} <= {threshold:.2f} (True)")

            # Right branch (False condition)
            if right is not None and name != "Leaf":
                right_name = f"{node_data[right][1]} <= {node_data[right][2]:.2f}" if node_data[right][1] != "Leaf" else f"Leaf: {self.outcome_at_node(right)}"
                if right_name not in node_id:
                    node_id[right_name] = counter
                    labels.append(right_name)
                    counter += 1
                source.append(node_id[node_name])
                target.append(node_id[right_name])
                values.append(1)
                hover_text.append(f"{name} > {threshold:.2f} (False)")

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

    def outcome_at_node(self, node):
        """
        Returns the predicted outcome at a leaf node.
        For classifiers, this returns the class with the highest probability.
        For regressors, this returns the predicted value.
        """
        if self.is_classifier:
            return f"Class {self.outcomes[np.argmax(self.tree_.value[node][0])]}"
        else:
            return f"Value {np.mean(self.tree_.value[node][0]):.2f}"
