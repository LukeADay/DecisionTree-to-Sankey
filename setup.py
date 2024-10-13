from setuptools import setup, find_packages

setup(
    name='DecisionTree_to_Sankey',
    version='0.1',
    description='A package to visualize decision trees as Sankey diagrams using Plotly.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Luke Day',
    author_email='luke.alexander.day@gmail.com',
    url='https://github.com/LukeADay/DecisionTree-to-Sankey',
    packages=find_packages(where='src'),  # Look for packages in the 'src' directory
    package_dir={'': 'src'},  # Tells setuptools where to find your package code
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'plotly',
        'seaborn',
    ],
    python_requires='>=3.6',
)
