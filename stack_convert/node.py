class Node:
  def __init__(self, name, value=0, children={}):
    self.name = name
    self.value = value
    self.children = children

  def add(self, frames, value):
    self.value += value

    if (frames and len(frames) > 0):
      head = frames[0]
      child = self.children[head] if self.children[head] else None
      if (child is None):
        child = Node(head)
        self.children[head] = child
      frames[0:1] = []
      child.add(frames, value)

  def serialize(self):
    res = {'name': self.name, 'value': self.value}

    children = []

    for key in self.children:
      children.append(self.children[key].serialize())

    if (len(children) > 0):
      res.children = children

    return res
