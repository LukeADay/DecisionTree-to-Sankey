Usage
=====

Here’s a quick example of how to use the `DecisionTree_to_Sankey` class:

.. code-block:: python

   from decisiontree_to_sankey import DecisionTree_to_Sankey
   from sklearn.tree import DecisionTreeClassifier
   import pandas as pd

   # Sample data
   data = pd.DataFrame({
       'Feature1': [1, 2, 3, 4],
       'Feature2': [5, 6, 7, 8]
   })
   target = [0, 1, 0, 1]

   # Train a decision tree
   clf = DecisionTreeClassifier()
   clf.fit(data, target)

   # Create and visualize the Sankey diagram
   dt_sankey = DecisionTree_to_Sankey(clf, data)
   dt_sankey.create_sankey()
