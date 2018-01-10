from .profile import Profile
import re
import logging

class Parser:
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__qualname__)
    self.profile = None

  def parseDTrace(self, filename):
    self.logger.debug("Opening [{0}] for parsing".format(filename))
    fh = open(filename, "r")

    # Open a new profile to contain everything in this file
    # Later, we'll have one of these per timestamp
    self.profile = Profile()

    for line in map(lambda line: line.rstrip('\n'), fh):

      # Possible states:
      # 1. No open stack
      #    a. We'll open a stack for a particular execname, if one is present
      #    b. We'll open a stack with no execname/header for the stack
      #    c. We'll skip comments
      #    d. Find an unknown construct, and note it on STDERR, but continue
      #    e. We'll parse an epoch timestamp, if present (or will we?)
      #    f. We'll parse a datetimestamp (or is that at each Profile?)
      # 2. The profile stack is already open, and we're either going to:
      #    a. Add a new frame to the stack
      #    b. Find the count for the stack as a whole and close the stack
      #    c. Detect the gap between a kernel/user stack, which we'll add as an '-' frame
      #    d. Find an unknown construct, and note it on STDERR, but continue

      # 1. Is there no open stack?
      if (not self.profile.stack_is_open):
        # 1c. Skip comment lines
        if re.search(r"^\s+?#", line):
          continue
        # Skip blank lines
        if re.search(r"^\s+?$", line):
          continue
        # This is likely identical - eliminate if so
        if re.search(r"^$", line):
          continue
        # 1a. Look for just an execname
        execm = re.search(r"^\s+?(\w+)$", line)
        if execm:
          execname = execm.group(1)
          self.logger.debug("OPENING STACK FOR EXECNAME: %s" % execname)
          self.profile.openStack(execname)
          # No frame to add yet - the next line should be the first frame
          continue
        # 1b. Look for a plain unadorned stack frame
        #     This will take the form of an unresolved hex address: 0x0123456789abcdef
        #     Or a resolved symbol + offset: genunix`cdev_ioctl+0x67
        frame = self._frame_parse(line)
        if frame is not None:
          # Make sure this is a recognizable frame
          if not re.search(r"^(\S+)`(\S+)$", frame):
            self.logger.warn("UNKNOWN LINE BETWEEN STACKS: %s", frame)
            continue
            self.logger.debug("OPENING STACK FOR PLAIN FRAME: %s" % frame)
          self.profile.openStack(frame)
          # ... and insert that first frame
          self.profile.addFrame(frame, None)
          continue
      #
      # 2. There is a currently open stack
      #
      else:
        # 2a. Add a new frame to the existing stack (factor out)
        frame = self._frame_parse(line)
        if frame is not None:
          # Make sure this is a recognizable frame
          if not re.search(r"^(\S+)`(\S+)|0x[\da-f]+$", frame):
            self.logger.warn("UNKNOWN LINE IN OPEN STACK: %s", frame)
            continue
          self.profile.addFrame(frame, None)
          continue
        # 2b. Find the count for the stack as a whole and close the stack
        stackfreqm = re.search(r"^\s+?(\d+)$", line)
        if stackfreqm:
          count = stackfreqm.group(1)
          self.profile.closeStack(count)
          continue
        # 2c. Detect the gap between a kernel/user stack, which we'll add as an '-' frame
        gapm = re.search(r"^\s+?$", line)
        if gapm:
          self.logger.debug("GAP FRAME BETWEEN KERNEL/USER STACKS")
          self.profile.addFrame('-', None)

    return self.profile

  def serializeProfile(self):
    """Serialize Profile Samples"""
    self.serialized = self.profile.samples.serialize()
    return self.serialized

  def encodeAsJSON(self):
    """Encode a Serialized Profile as JSON"""
    import json
    #encoded = json.dumps(self.serialized,sort_keys=True)
    encoded = json.dumps(self.serialized, sort_keys=True, indent=4, separators=(',', ': '))
    return encoded

  def _frame_parse(self, text):
    # Look for a plain unadorned stack frame
    #     This will take the form of an unresolved hex address: 0x0123456789abcdef
    #     Or a resolved symbol + offset: genunix`cdev_ioctl+0x67
    framem = re.search(r"^\s+?(0x[0-9a-f]+|\w+`\w+\+0x[0-9a-f]+)", text)
    if framem:
      frame = framem.group(1)
      # Strip the frame down
      # Strip leading whitespace
      frame = re.sub(r'^\s*', '', frame)
      # Strip offset into function
      frame = re.sub(r'\+[^+]*$', '', frame)
      # Remove args from C++ function names
      frame = re.sub(r'(::.*)[(<].*', r'\1', frame)
      return frame
    else:
      return None


