from .node import Node


class Profile:
  def __init__(self, samples=Node('root'), stack=[]):
    self.samples = samples
    self.stack = stack
    self.stack_is_open = 0
    self.name = None

  def openStack(self, name):
    self.stack_is_open = 1
    self.name = name

  def addFrame(self, func, mod):
    # TODO: skip process name and some punctuation
    # prepend function to list
    self.stack.insert(0, func)

  def closeStack(self, value):
    self.stack.insert(0, self.name)
    self.samples.add(self.stack, value)

    self.stack([])
    self.name(None)
    self.stack_is_open(0)


