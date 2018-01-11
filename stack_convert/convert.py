import argparse
from stack_convert import Parser
import logging
import pyaml

class Convert:
  """Orchestrates Parsing/Collapsing of stack data and emitting in JSON format
  """
  def __init__(self, config):
    self.config = config

  def run(self):
    self.stackparser = Parser()
    self.stackparser.parseDTrace(self.config.inputFile)
    self.stackparser.serializeProfile()
    json_data = self.stackparser.encodeAsJSON()
    print(json_data)
    self.stackparser = None


class LoggingConfig:
  def __enter__(self, filename="log_config.yaml"):
    logging.config.dictConfig( pyaml.load(filename))
  def __exit__(self, *exc):
    logging.shutdown()


class ApplicationConfig:
  def __enter__(self):
    # Build os.environ defaults.
    # Load files.
    # Build ChainMap from environs and files.
    # Parse command-line arguments.
    argparser = argparse.ArgumentParser(description="Convert stacks into JSON")
    argparser.add_argument("-i", "--inputFile", action="store", type=str,
                           help="file containing raw stack data to parse")
    argparser.add_argument("-t", "--inputType", action="store", type=str, default="",
                           help="type of input data (selects correct parser)")
    argparser.add_argument("-c", "--stackCount", action="store", type=int,
                           help="number of stacks to process before exiting")
    namespace = argparser.parse_args()
    return namespace

  def __exit__(self, *exc):
    pass

