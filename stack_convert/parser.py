from .profile import Profile
import re

class Parser:
  def __init__(self):
    self.profile = None

  def parseDTrace(self, filename):
    print("Opening [%s] for parsing", filename)
    fh = open(filename, "r")

    self.profile = Profile()

    for line in fh:
      line.rstrip('\n')

      if re.search(r"^\s*$", line):
        continue
      if re.search(r"^$", line):
        continue

      m = re.search(r"^\s*(\d+)$", line)
      if m:
        count = m[0]
        if (profile.stack_is_open):
          self.profile.closeStack(count)
        else:
          print("ERROR: %s", line)
        continue

      frame = line

      # Strip leading whitespace
      frame = re.sub(r'^\s*', '', frame)
      # Strip offset into function
      frame = re.sub(r'\+[^+]*$', '', frame)
      # Remove args from C++ function names
      frame = re.sub(r'(::.*)[(<].*', r'\1', frame)
      # Denote separator between kernel and user stacks with '-'
      if re.search(r"^$", frame):
        frame = "-"

      if not re.search(r"^(\S+)`(\S+)$", frame):
        print("UNKNOWN LINE: %s", frame)
        continue

      if (self.profile.stack_is_open):
        print("Sending to profile addFrame with: (%s, None)", frame)
        self.profile.addFrame(frame, None)
      else:
        self.profile.openStack('kernel')
        print("Sending to profile addFrame with: (%s, None)", frame)
        self.profile.addFrame(frame, None)

    return self.profile

  def serializeProfile(self):
    """Serialize Profile Samples"""
    return self.profile.samples.serialize()

  def encodeAsJSON(self, serializedProfile=None):
    """Encode a Serialized Profile as JSON"""
    import json
    encoded = json.dumps(serializedProfile)
    return encoded
