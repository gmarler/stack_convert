from setuptools import setup, find_packages

setup(
  name='stack_convert',
  version='0.0.1',
  license='MIT',
  description='Stack Conversion to D3 FlameGraph JSON Format',

  author='Gordon Marler',
  author_email='gmarler@gmarler.com',

  packages=find_packages(where='stack_convert'),
  package_dir={'': 'stack_convert'},

  install_requires=['pytest', 'pytest-mock', 'pytest-datafiles', 'pyaml'],
  tests_require=['pytest', 'pytest-mock', 'pytest-datafiles', 'pyaml'],

  scripts=['bin/stack_convert'],
)
