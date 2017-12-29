"""Test the Node object."""
from .context import stack_convert
from stack_convert import Node

def test_defaults():
  """Using no parameters should invoke defaults."""
  n1 = Node("junk")
  n2 = Node("junk", 0, {})
  assert n1.name == n2.name
  assert n1.value == n2.value
  assert n1.children == n2.children

def test_single_node():
  n1 = Node("lwp_start", 5)
  assert n1.name == "lwp_start"
  assert n1.value == 5

def test_double_node():
  n1 = Node("lwp_start", 5)
  n2 = Node("lwp_park", 5, {'lwp_start': n1})
  assert len(n2.children) == 1
  assert n1.value == 5
  assert n2.value == 5
  assert n2.children['lwp_start'] == n1
  assert n2.children['lwp_start'].value == 5
