"""Setup module for packaging the iceberg library"""

from setuptools import setup, find_packages

import iceberg

setup(
    name='iceberg',
    version=iceberg.__version__,
    description='Musicology-Inspired Population Size Estimation',
    author='William Watson',
    author_email='wcwatson92@gmail.com',
    packages=find_packages(),
    package_data={'iceberg': './docs/*'}
)
