from .node import Node
import logging


class Profile:
  def __init__(self, samples=None, stack=None):
    self.logger = logging.getLogger(self.__class__.__qualname__)
    if stack is None:
      stack = []
    if samples is None:
      self.samples = Node('root')
    self.stack = stack
    self.stack_is_open = False
    self.name = None

  def openStack(self, name):
    """name: the name of the top level Node in the profile"""
    self.stack_is_open = True
    self.name = name

  def addFrame(self, func, mod):
    # TODO: skip process name and some punctuation
    # prepend function to list
    self.stack.insert(0, func)

  def closeStack(self, value):
    # self.stack.insert(0, self.name)
    self.samples.add(self.stack, value)

    self.stack = []
    self.name = None
    self.stack_is_open = False


