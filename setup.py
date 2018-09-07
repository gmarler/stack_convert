from setuptools import setup

setup(
  name='stack_convert',
  version='0.0.2',
  license='MIT',
  description='Stack Conversion to D3 FlameGraph JSON Format',

  author='Gordon Marler',
  author_email='gmarler@gmarler.com',

  packages=['stack_convert'],

  install_requires=['pytest', 'pytest-mock', 'pytest-datafiles', 'pyaml'],
  tests_require=['pytest', 'pytest-mock', 'pytest-datafiles', 'pyaml'],

  scripts=['bin/stack_convert'],
)
