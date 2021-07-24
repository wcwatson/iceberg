"""Setup module for packaging the iceberg-est library"""

from setuptools import setup, find_packages
import codecs
import os
import pathlib


# Auxiliary functionality to read version number
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


# Find long project description in README
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')


# Run setup
setup(
    name='iceberg-est',
    version=get_version('iceberg/__init__.py'),
    description='Musicologically motivated population size estimation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wcwatson/iceberg',
    author='William Watson',
    author_email='wcwatson92@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6, <4',
    install_requires=['numpy']
)
