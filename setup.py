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
        "numpy>=1.21.0,<=2.1.3",
        "pandas>=1.3.0,<=2.2.3",
        "scikit-learn>=0.24.0,<=1.5.2",
        "plotly>=5.0.0,<=5.24.1",
    ],
    extras_require={
        "testing": ["pytest>=6.0"],
        "dev": ["black", "flake8", "mypy"]
    },
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

from setuptools import setup, find_packages

setup(
    name="tree-sankey-visualizer",
    version="0.2",
    description="A Python library for visualizing decision trees as Sankey diagrams.",
    author="Luke Day",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.21.0,<=2.1.3",
        "pandas>=1.3.0,<=2.2.3",
        "scikit-learn>=0.24.0,<=1.5.2",
        "plotly>=5.0.0,<=5.24.1",
    ],
    extras_require={
        "testing": ["pytest>=6.0"],
        "dev": ["black", "flake8", "mypy"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
