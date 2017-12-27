import Node

class Profile:
  def __init__(self, samples=Node('root'), stack=[]):
    self.samples = samples
    self.stack = stack
    self.stack_is_open = 0
    self.name = None

  def openStack(self,name):
    self.stack_is_open = 1
    self.name = name

