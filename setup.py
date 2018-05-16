from setuptools import setup, find_packages

setup(name='dataprov',
      version='0.1',
      description='Automatic provenance metadata creator',
      url='...',
      author='Felix Bartusch',
      author_email='felix.bartusch@uni-tuebingen.de',
      license='TODO',
      packages=find_packages(),
      entry_points = {
          'console_scripts': ['dataprov=dataprov.__main__:main']
      },
      install_requires=[
          'future',
          'six',
          'argparse',
          'lxml',
          'configparser',
          'docker',
          'html5lib',
          'networkx',
      ],
      include_package_data=True,
      zip_safe=False)

