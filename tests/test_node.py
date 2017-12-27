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
