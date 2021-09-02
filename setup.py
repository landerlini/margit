from distutils.core import setup 
import setuptools
from glob import glob 

with open ("README.md", "r") as readme:
  long_description = readme.read() 

setup ( 
  name = 'margit',
  version = '0.1',
  description = 'Simplified CLI for Dirac job submission',
  long_description = long_description, 
  long_description_content_type = "text/markdown", 
  author = 'Lucio Anderlini',
  author_email = 'Lucio.Anderlini@cern.ch',
  url = 'https://github.com/landerlini/margit',
  packages = setuptools.find_packages(),
  include_package_data=False,
  package_data={'margit': ['templates/*.*', '*.sh']},
  scripts = glob("scripts/*"), 
  classifiers = [
    "Programmin Language :: Python :: 3"
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  install_requires = [
      "numpy", 
      "PyYAML>=5.3.1", 
      "wheel",
      ],
  entry_points={  # Optional
    'console_scripts': [
      'margit=margit.__main__:main',
      ],
    },
)


