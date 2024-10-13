#%%
### Example using the boston housing dataset to demontrate regression
from decisiontree_to_sankey import DecisionTree_to_Sankey
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import plotly.graph_objects as go
from sklearn.datasets import fetch_openml

#%%
# Load the Boston Housing dataset
boston = fetch_openml(data_id=531, as_frame=True)  # Alternative source for Boston Housing dataset

# Create a DataFrame for easier handling
X = boston.data
y = boston.target  # This is the median house value

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a regression decision tree
regressor = DecisionTreeRegressor(random_state=42, max_depth=3)  # Limiting tree depth for simplicity
regressor.fit(X_train, y_train)

# Create a Sankey diagram for the regression tree
dt_sankey = DecisionTree_to_Sankey(regressor, X_train)
dt_sankey.create_sankey(title="Regression Tree Sankey Diagram (Boston Housing Dataset)")

# %%
