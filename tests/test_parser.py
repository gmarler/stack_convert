"""Test the Parser object."""
import os
import pytest
from .context import stack_convert
from stack_convert import Parser

FIXTURE_DIR = os.path.join(
  os.path.dirname(os.path.realpath(__file__)),
  'test_data',
)

@pytest.mark.datafiles(
  os.path.join(FIXTURE_DIR, 'kernel-stack-simple.raw')
)
def test_simple_DTrace_parse(datafiles):
  path = str(datafiles)
  assert(datafiles / 'kernel-stack-simple.raw').check(file=1)
  parser = Parser()
  for datafile in datafiles.listdir():
   profile = parser.parseDTrace(str(datafile))
   print(profile)
