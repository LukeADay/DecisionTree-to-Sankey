# Import required libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import plotly.graph_objects as go
from sklearn.tree import _tree


class DecisionTree_to_Sankey():
    """
    Class takes a trained decision tree (regression or classification) and produces a plotly based Sankey Diagram

    Inputs:
        - Trained decision tree (clf)
        - (optional) title: the title of the interactive plotly sankey diagram

    Outputs:
        - A plotly visualisation, a Sankey diagram showing the movement through nodes and branches to the final predicted class

    """
    def __init__(self, clf, X):
        if X.empty:
            raise ValueError("Input dataset is empty.")
        self.clf = clf
        self.X = X
        
    # Extract the decision tree structure
        self.tree_ = clf.tree_

    # Function to traverse the tree and collect node information
    def extract_tree_structure(self, tree, feature_names):
        node_info = []
        
        def recurse(node, depth):
            if tree.feature[node] != _tree.TREE_UNDEFINED:
                # Not a leaf node, add to node_info
                name = feature_names[tree.feature[node]]
                threshold = tree.threshold[node]
                node_info.append((depth, name, threshold, tree.children_left[node], tree.children_right[node]))
                recurse(tree.children_left[node], depth + 1)
                recurse(tree.children_right[node], depth + 1)
            else:
                # Leaf node
                node_info.append((depth, "Leaf", None, None, None))
        
        recurse(0, 0)
        return node_info
    
    def create_sankey(self, title = "Decision Tree Sankey Diagram with Leaf Nodes and Binary Splits"):

        # Extract the tree structure
        node_data = self.extract_tree_structure(self.clf.tree_, self.X.columns)

        # Prepare the data for a Sankey diagram
        labels = []
        source = []
        target = []
        values = []
        hover_text = []  # To store custom hover text for the branches

        # Get the predicted classes for leaf nodes (outcomes)
        outcomes = self.clf.classes_  # Predicted class labels

        # Fill the Sankey data based on the node structure
        node_id = {}
        counter = 0

        for idx, (depth, name, threshold, left, right) in enumerate(node_data):
            if name != "Leaf":
                node_name = f"{name} <= {threshold:.2f}"
            else:
                # For leaf nodes, add the final predicted outcome
                node_name = f"Leaf: Class {outcomes[np.argmax(self.tree_.value[idx][0])]}"  # Predicted class for the leaf node
            
            if node_name not in node_id:
                node_id[node_name] = counter
                labels.append(node_name)
                counter += 1
            
            # Left branch (True condition)
            if left is not None and name != "Leaf":
                if node_data[left][1] != "Leaf":
                    left_name = f"{node_data[left][1]} <= {node_data[left][2]:.2f}"  # Left condition
                else:
                    left_name = f"Leaf: Class {outcomes[np.argmax(self.tree_.value[left][0])]}"  # Leaf node outcome
                
                if left_name not in node_id:
                    node_id[left_name] = counter
                    labels.append(left_name)
                    counter += 1
                
                source.append(node_id[node_name])
                target.append(node_id[left_name])
                values.append(1)
                hover_text.append(f"{name} <= {threshold:.2f} (True)")  # Hover text for the left branch
            
            # Right branch (False condition)
            if right is not None and name != "Leaf":
                if node_data[right][1] != "Leaf":
                    right_name = f"{node_data[right][1]} <= {node_data[right][2]:.2f}"  # Right condition
                else:
                    right_name = f"Leaf: Class {outcomes[np.argmax(self.tree_.value[right][0])]}"  # Leaf node outcome
                
                if right_name not in node_id:
                    node_id[right_name] = counter
                    labels.append(right_name)
                    counter += 1
                
                source.append(node_id[node_name])
                target.append(node_id[right_name])
                values.append(1)
                hover_text.append(f"{name} > {threshold:.2f} (False)")  # Correct hover text for the right branch

        # Create the Sankey diagram with the correct hover text
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
                hovertemplate='%{customdata}<extra></extra>'  # Use custom hover text in hovertemplate
            )
        ))

        fig.update_layout(title_text=title, font_size=10)
        self.fig = fig
        fig.show()
        


