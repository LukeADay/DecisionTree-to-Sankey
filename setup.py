from setuptools import setup, find_packages

setup(
    name='decisiontree-to-sankey',
    version='0.1',
    description='A package to visualize decision trees as Sankey diagrams using Plotly.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Luke Day',
    author_email='luke.alexander.day@gmail.com',
    url='https://github.com/LukeADay/DecisionTree-to-Sankey',
    packages=['decisiontree_to_sankey'],  # Explicitly specify the package
    package_dir={'decisiontree_to_sankey': 'src'},    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'plotly',
        'seaborn',
    ],
    python_requires='>=3.6',
)
