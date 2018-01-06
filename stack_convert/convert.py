import argparse
from .context import stack_convert
from stack_convert import Parser

class Convert:
  """Orchestrates Parsing/Collapsing of stack data and emitting in JSON format
  """
  def __init__(self):
    argparser = argparse.ArgumentParser(description="Convert stacks into JSON")
    argparser.add_argument("-i", "--inputFile", action="store", type=str,
                        help="raw stack data to parse")
    argparser.add_argument("-t", "--inputType", action="store", type=str, default="",
                        help="type of input data (selects correct parser)")
    self.config = argparser.parse_args()

  def run(self):
    self.stackparser = Parser()
    self.stackparser.parseDTrace(self.config.inputFile)
    self.stackparser.serializeProfile()
    json_data = self.stackparser.encodeAsJSON()
    print(json_data)
