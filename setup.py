"""
Setup script for QPCA-EnDCF package.
"""

from setuptools import setup, find_packages

setup(
    name="qpca-endcf",
    version="0.1.0",
    description="QPCA Ensemble Data Consistency Filter for data assimilation",
    author="Rylan Spence",
    author_email="rylan.spence@utexas.edu",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "matplotlib>=3.3.0",
    ],
    python_requires=">=3.8",
)
