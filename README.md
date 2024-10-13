# DecisionTree-to-Sankey :evergreen_tree: :leaves:

Decision/Classification trees are great for interpretability - allowing us to see the paths of feature values that lead to a predicted outcome. But in practice decision trees are often complex and plotting the tree itself is not always readable due to overlapping text and boxes.

The `DecisionTree_to_Sankey` class aims to address this by presenting the decision tree as an interactive `plotly` Sankey Diagram. The nodes can be dragged around when labels overlap and the user can hover over branches to see the conditions that lead to each node.

## Usage

Clone the repository and install the environment in `environment.yml`. 

1. Clone this repository: `git clone https://github.com/LukeADay/DecisionTree-to-Sankey.git`
2. Create the conda environment: `conda env create -f environment.yml`
3. Activate it with `conda activate tree-sankey-visualizer`
4. Import the `DecisionTree_to_Sankey` class from `src/DecisionTree_To_Sankey`.
5. Initialise the class by passing it a trained decision tree `clf`.
6. Call the `create_sankey()` method to produce the interactive plotly sankey.

The following shows an example of the output. Although boxes overlap, the interactive version allows nodes the be dragged around:
![Sankey Diagram](examples/sankey_diagram.png)



**Examples can be found in the `examples` folder**.

## Structure of repository

```
├── LICENSE
├── README.md
├── environment.yml
├── examples
│   ├── __init__.py
│   ├── environment.yml
│   ├── penguine_dataset_example.ipynb
│   └── penguine_dataset_example.py
├── src
│   ├── DecisionTree_To_Sankey.py
│   ├── __init__.py
└── tests

```

The `DecisionTree_To_Sankey` class creates the sankey diagram. Examples can be found in the examples folder.