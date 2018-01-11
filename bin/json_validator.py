#!/usr/bin/env python

import json
import sys

filename = sys.argv[1]


def parse(filename):
  with open(filename) as f:
    try:
      return json.load(f)
    except ValueError as e:
      print('invalid json: %s' % e)
      return None

parse(filename)