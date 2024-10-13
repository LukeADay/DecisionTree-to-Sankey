#
### Example as a script - see ipynb for the same example with more detailed comments
# %%
from decisiontree_to_sankey import DecisionTree_to_Sankey
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import plotly.graph_objects as go
from sklearn.tree import _tree

# Load penguins dataset from seaborn
import seaborn as sns

#%%
# Load the penguins dataset from seaborn
# Fit a basic decision tree
# Return accuracy
# Note this is an example so hyperparameters are not tuned
penguins = sns.load_dataset("penguins")

# Drop rows with missing values
penguins = penguins.dropna()

# Convert categorical columns to 'category' dtype
penguins['species'] = penguins['species'].astype('category')
penguins['island'] = penguins['island'].astype('category')
penguins['sex'] = penguins['sex'].astype('category')

# Separate features and target
X = penguins.drop('species', axis=1)
y = penguins['species']

# Encode categorical variables in X (island and sex) with pandas' categorical codes
X['island'] = X['island'].cat.codes
X['sex'] = X['sex'].cat.codes

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state=42)

# Fit the model
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

#%%
###

dt = DecisionTree_to_Sankey(clf, X)

dt.create_sankey()

# Incase it is required to plot again later
#dt.fig.show()

# %%
