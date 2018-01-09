"""Test the Parser object."""
import os
import pytest
from .context import stack_convert
from stack_convert import Parser

FIXTURE_DIR = os.path.join(
  os.path.dirname(os.path.realpath(__file__)),
  'test_data',
)

@pytest.fixture()
def kernel_stack_simple_json():
  return r'{"children": [{"children": [{"children": [{"children": [{"name": "unix`mach_cpu_idle", "value": 19199}], "name": "unix`cpu_idle", "value": 19199}], "name": "unix`idle", "value": 19199}], "name": "unix`thread_start", "value": 19199}], "name": "root", "value": 19199}'

@pytest.mark.datafiles(
  # os.path.join(FIXTURE_DIR, 'kernel-stack-simple.raw'),
  #os.path.join(FIXTURE_DIR, 'kernel-stacks2.raw'),
  os.path.join(FIXTURE_DIR, 'kernel-stack-simple2.raw'),
)
def test_simple_DTrace_parse(datafiles,kernel_stack_simple_json):
  path = str(datafiles)
  # assert(datafiles / 'kernel-stack-simple.raw').check(file=1)

  for datafile in datafiles.listdir():
   parser = Parser()
   profile = parser.parseDTrace(str(datafile))
   #print(profile)
   parser.serializeProfile()
   json_data = parser.encodeAsJSON()
   #assert json_data == kernel_stack_simple_json
   # print(json_data)
   # TODO: Convert back to a data structure and compare again
   # import json
   # json_string = str(kernel_stack_simple_json)
   # print(json_string)
   # expected_data = json.JSONDecoder.decode(json_string)
   # actual_data = json.JSONDecoder.decode(json_data)
   # assert actual_data == expected_data

@pytest.mark.datafiles(
  os.path.join(FIXTURE_DIR, 'kernel-stack-simple-unresolved.raw'),
)
def test_unresolved_address_parse(datafiles):
  path = str(datafiles)
  assert(datafiles / 'kernel-stack-simple-unresolved.raw').check(file=1)

  for datafile in datafiles.listdir():
   parser = Parser()
   profile = parser.parseDTrace(str(datafile))
   #print(profile)
   # Now that we've parsed the data, look for a Node with name "0x10401b18"
   serialized = parser.serializeProfile()
   assert serialized['children'][0]['children'][0]['children'][0]['children'][0]['name'] == "0x10401b18"
   json_data = parser.encodeAsJSON()
   #assert json_data == kernel_stack_simple_json
   #print(json_data)