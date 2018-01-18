"""Test the Parser object."""
import os
import pytest
from .context import stack_convert
from stack_convert import Parser

FIXTURE_DIR = os.path.join(
  os.path.dirname(os.path.realpath(__file__)),
  'test_data',
)

# Get the function name from stack frame framedepth of serialized
def frame_x_funcname(serialized, framedepth):
  if framedepth == 0:
    return serialized[0]['name']
  current = serialized
  for i in range(0, framedepth):
    current = current['children'][0]
  return current['name']

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

@pytest.mark.datafiles(
  os.path.join(FIXTURE_DIR, 'user-return-removal.raw'),
)
def test_user_return_removal(datafiles):
  path = str(datafiles)
  assert(datafiles / 'user-return-removal.raw').check(file=1)

  expected_funcnames = [
    'BloombergLP::bdlb::NullableValue<bool>::makeValue<bool>',
    'js::Invoke',
    'bsl::map<BloombergLP::bdlt::Date,double,std::less<BloombergLP::bdlt::Date>,bsl::allocator<bsl::pair<const BloombergLP::bdlt::Date,double> > >::operator[]',
    'double_to_decimal',
    'UTC',
  ]

  for datafile in datafiles.listdir():
   parser = Parser()
   profile = parser.parseDTrace(str(datafile))
   #print(profile)
   # Now that we've parsed the data, look for each Node to have had their return type removed,
   # but the function name properly kept
   serialized = parser.serializeProfile()
   # assert serialized['children'][0]['children'][0]['children'][0]['children'][0]['name'] == "0x10401b18"
   # print(frame_x_funcname(serialized, 1))
   # assert serialized['children'][0]['name'] == 'BloombergLP::bdlb::NullableValue<bool>::makeValue<bool>'
   assert frame_x_funcname(serialized, 1) == 'BloombergLP::bdlb::NullableValue<bool>::makeValue<bool>'
   for stackdepth in (1, 5):
     assert frame_x_funcname(serialized, stackdepth) == expected_funcnames[stackdepth - 1]