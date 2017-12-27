"""Test the Node object."""
from .context import stack_convert
from stack_convert import Node

def test_defaults():
  """Using no parameters should invoke defaults."""
  n1 = Node("junk")
  n2 = Node("junk", 0, {})
  assert n1 == n2
