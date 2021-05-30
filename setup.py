"""Setup module for packaging the iceberg-est library"""

from setuptools import setup, find_packages
import pathlib

import iceberg

# Find long project description in README
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Run setup
setup(
    name='iceberg-est',
    version=iceberg.__version__,
    description='Musicologically motivated population size estimation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wcwatson/iceberg',
    author='William Watson',
    author_email='wcwatson92@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    packages=find_packages(),
    package_data={'iceberg': './docs/*'},
    python_requires='>=3.8, <4',
    install_requires=['numpy']
)
