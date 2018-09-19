from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tnr', 
    version='1.0.0',  # Required

    description='Transient Name Resolver',  

    long_description=long_description, 
    long_description_content_type='text/markdown', 

   # url='https://github.com/pypa/sampleproject',  # Optional

    author='Volodymyr Savchenko', 

    author_email='vladimir.savchenko@gmail.com',

    classifiers=[
        'Development Status :: 3 - Alpha',
     #   'Intended Audience :: Developers',
     #   'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='astronomy',  

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  

    packages=find_packages(exclude=['contrib', 'docs', 'tests']), 

    install_requires=['peppercorn'],  # Optional

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

   # package_data={  # Optional
   #     'sample': ['package_data.dat'],
   # },

  #  data_files=[('my_data', ['data/data_file'])],  # Optional

  #  entry_points={  # Optional
  #      'console_scripts': [
  #          'sample=sample:main',
  #      ],
  #  },

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
 #   project_urls={  # Optional
 #       'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
 #       'Funding': 'https://donate.pypi.org',
 #       'Say Thanks!': 'http://saythanks.io/to/example',
 #       'Source': 'https://github.com/pypa/sampleproject/',
 #   },
)
