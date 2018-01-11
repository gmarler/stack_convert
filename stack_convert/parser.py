from .profile import Profile
import re
import logging

class Parser:
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__qualname__)
    self.profile = None

  def parseDTrace(self, filename, stackMax):
    self.logger.debug("Opening [{0}] for parsing".format(filename))
    fh = open(filename, "r")
    stacksProcessed = 0

    # Open a new profile to contain everything in this file
    # Later, we'll have one of these per timestamp
    self.profile = Profile()

    for line in map(lambda line: line.rstrip('\n'), fh):

      # Possible states:
      # 1. No open stack
      #    a. We'll open a stack for a particular execname, if one is present
      #    b. We'll open an unadorned stack (no header for the stack)
      #    c. Or open a stack for a PID/TID variant of the header
      #    d. We'll skip comments
      #    e. Find an unknown construct, and note it on STDERR, but continue
      #    f. We'll parse an epoch timestamp, if present (or will we?)
      #    g. We'll parse a datetimestamp (or is that at each Profile?)
      # 2. The profile stack is already open, and we're either going to:
      #    a. Add a new frame to the stack
      #    b. Find the count for the stack as a whole and close the stack
      #    c. Detect the gap between a kernel/user stack, which we'll add as an '-' frame
      #    d. Find an unknown construct, and note it on STDERR, but continue

      # 1. Is there no open stack?
      if not self.profile.stack_is_open:
        # 1d. Skip comment lines
        if re.search(r"^(?:\s+)?#", line):
          continue
        # Skip blank lines
        if re.search(r"^(?:\s+)?$", line):
          continue
        # This is likely identical - eliminate if so
        if re.search(r"^$", line):
          continue
        # 1g. Parse a datetimestamp variant
        dtm = re.search(r"""
          ^ \d{4} \s+             # Year
            (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)
            \s+
            \d+ \s+               # Day of Month
            \d{2}:\d{2}:\d{2} \s+ # HH:MM:SS
            \[ \d+ \]             # Epoch secs
          $
          """,
          line,
          re.VERBOSE
        )
        if dtm:
          # We'll handle datetimestamps later, for now just skip them
          continue
        # 1c. Handle PID/TID header variant
        pidtidm = re.search(r"^PID:(\d+)\s+(\d+)", line)
        if pidtidm:
          pid = pidtidm.group(1)
          tid = pidtidm.group(2)
          pid_tid_header = "%s/%s" % (pid, tid)
          self.logger.debug("OPENING STACK FOR PID/TID VARIANT: %s" % pid_tid_header)
          self.profile.openStack("PID_TID_PLACEHOLDER")
          # No frame to add yet - the next line should be the first frame
          continue
        # 1a. Look for just an execname
        execm = re.search(r"^(?:\s+)?(\w+)$", line)
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
          if not re.search(r"^\w+|0x[\da-f]+$", frame):
            self.logger.warn("UNKNOWN LINE BETWEEN STACKS: %s" % frame)
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
        # 2b. Find the count for the stack as a whole and close the stack
        stackfreqm = re.search(r"^(?:\s+)?(\d+)$", line)
        if stackfreqm:
          count = stackfreqm.group(1)
          self.profile.closeStack(count)
          stacksProcessed += 1
          if stacksProcessed >= stackMax:
            break
          continue
        # 2a. Add a new frame to the existing stack (factor out)
        frame = self._frame_parse(line)
        if frame is not None:
          # Make sure this is a recognizable frame
          if not re.search(r"^\w+|0x[\da-f]+$", frame):
            self.logger.warn("UNKNOWN LINE IN OPEN STACK: %s", frame)
            continue
          self.profile.addFrame(frame, None)
          continue
        # 2c. Detect the gap between a kernel/user stack, which we'll add as an '-' frame
        gapm = re.search(r"^(?:\s+)?$", line)
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
    # Try to strip the test down before parsing it further
    # Strip leading whitespace
    text = re.sub(r'^\s*', '', text)
    # Strip offset into function
    text = re.sub(r'\+[^+]*$', '', text)
    # Remove everything up to the function name
    #text = re.sub(r'.+?(\S+[(])', r'\1', text)
    # Remove args from C++ function names
    #text = re.sub(r'.+(::.*)[(<].*', r'\1', text)
    # Look for a plain unadorned stack frame
    # Remove args from C++ function names
    text = re.sub(r'([^(]+?)[(].+$', r'\1', text)
    # Strip off initial base return types from functions
    text = re.sub(r'^(?:int|void|char|unsigned|long|long long|bool|const)(?:(?:\s+)?(?:[\*]+)?(?:\s+)?)?', '', text)
    #     This will take the form of an unresolved hex address: 0x0123456789abcdef
    #     Or a resolved symbol + offset: genunix`cdev_ioctl+0x67
    framem = re.search(
      # r"""
      #   ^(?:\s+)?              # Possible whitespace
      #   (                      #  What we want to capture
      #      0x[0-9a-f]+ |       # Either an unresolved address
      #      (?:\w+`)?           # Or a resolved address with optional module prefix
      #      \w+                 # Followed by the resolved name
      #      (?:\+0x[0-9a-f]+)?  # and an optional offset into it
      #   )
      # """,
      r"""
        (.+)
      """,
      text,
      re.VERBOSE
    )
    if framem:
      frame = framem.group(1)

      return frame
    else:
      return None


