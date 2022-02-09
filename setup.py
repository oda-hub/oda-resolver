from setuptools import setup, find_packages  # type: ignore
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='tnr', 
    version='1.0.0',

    description='Transient Name Resolver',  

    long_description=long_description, 
    long_description_content_type='text/markdown', 

    author='Volodymyr Savchenko', 

    author_email='vladimir.savchenko@gmail.com',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='astronomy',  


    packages=find_packages(exclude=['contrib', 'docs', 'tests']), 

    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage', 'pytest-flask'],
    },

)
