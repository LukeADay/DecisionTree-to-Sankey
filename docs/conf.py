import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Debugging: Try importing the module directly in conf.py
try:
    from decisiontree_to_sankey import DecisionTree_to_Sankey
    print("Module imported successfully!")
except ImportError as e:
    print(f"Failed to import module: {e}")

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'decisiontree-to-sankey'
copyright = '2024, Luke Day'
author = 'Luke Day'
release = '0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',     # Automatically pull in docstrings from code
    'sphinx.ext.napoleon',    # For Google-style and NumPy-style docstrings
    'sphinx_rtd_theme',       # Use the Read the Docs theme
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'  # Switch from 'alabaster' to 'sphinx_rtd_theme' for Read the Docs theme
html_static_path = ['_static']

# -- Autodoc Configuration ---------------------------------------------------
# This allows autodoc to work and generate documentation from your code docstrings.

autodoc_default_options = {
    'members': True,           # Document class members
    'undoc-members': True,     # Include undocumented members (if applicable)
    'private-members': False,  # Do not document private members (starting with _)
    'special-members': False,  # Skip special members like __init__
    'inherited-members': True, # Include inherited members if applicable
}