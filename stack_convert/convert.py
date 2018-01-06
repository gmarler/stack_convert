import argparse
from .context import stack_convert
from stack_convert import Parser
import logging
import yaml

class Convert:
  """Orchestrates Parsing/Collapsing of stack data and emitting in JSON format
  """
  def __init__(self):
    argparser = argparse.ArgumentParser(description="Convert stacks into JSON")
    argparser.add_argument("-i", "--inputFile", action="store", type=str,
                        help="file containing raw stack data to parse")
    argparser.add_argument("-t", "--inputType", action="store", type=str, default="",
                        help="type of input data (selects correct parser)")
    self.config = argparser.parse_args()

  def run(self):
    self.stackparser = Parser()
    self.stackparser.parseDTrace(self.config.inputFile)
    self.stackparser.serializeProfile()
    json_data = self.stackparser.encodeAsJSON()
    print(json_data)


class LoggingConfig:
  def __enter__(self, filename="log_config.yaml"):
    logging.config.dictConfig( yaml.load(filename))
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
    namespace = argparser.parse_args()
    return namespace

  def __exit__(self, *exc):
    pass