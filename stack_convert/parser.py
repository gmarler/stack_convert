from .profile import Profile
import re

class Parser:
  def raw(self,filename):
    fh = open(filename,"r")
    for line in fh:
      line.rstrip('\n')

      if re.search(r"^\s*$", line):
        continue
      if re.search(r"^$", line):
        continue
      m = re.search(r"^\s*(\d+)$", line)
      if m:
        count = m[0]
