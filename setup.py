from setuptools import setup, find_packages

setup(
    name='decisiontree-to-sankey',
    version='0.2',
    description='A package to visualize decision trees as Sankey diagrams using Plotly.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Luke Day',
    license='MIT',
    author_email='luke.alexander.day@gmail.com',
    url='https://github.com/LukeADay/DecisionTree-to-Sankey',
    packages=find_packages(where='src'),  # Locate packages in the 'src' directory
    package_dir={'': 'src'},  # Root-level package mapping to 'src'
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'plotly',
        'seaborn',
    ],
    python_requires='>=3.6',
)
