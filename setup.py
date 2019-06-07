import sys
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


if sys.version_info < (3, 4):
    sys.exit('Sorry, Python < 3.4 is not supported')

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
      name='pysuez',
      version='0.1.12',
      description='Get your water consumption data from your Suez account (www.toutsurmoneau.fr)',
      long_description=long_description,
      author='Farid N27',
      author_email='pySuezWater@ooii.io',
      url='https://github.com/ooii/pySuez/releases/tag/0.1.12',
      package_data={'': ['LICENSE']},
      include_package_data=True,
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'pysuez = pysuez.__main__:main'
          ]
      },
      license='Apache 2.0',
      install_requires=['regex', 'requests', 'datetime'],
      classifiers=[
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ]
)
