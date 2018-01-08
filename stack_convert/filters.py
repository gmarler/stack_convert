import logging.filter

class SingleLevelFilter(logging.filter):
  def __init__(self, passlevel, reject):
    self.passlevel = passlevel
    self.reject = reject

  def filter(self, record):
    if self.reject:
      return(record.levelno != self.passlevel)
    else:
      return(record.levelno == self.passlevel)
