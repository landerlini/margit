import sys 
import os.path
from functools import wraps

import margit.core

cli_commands = {}

def cli_command (f):
  global cli_commands 
  cli_commands [f.__name__] = f


subpilot = os.path.join(
    os.path.split (os.path.abspath(__file__))[0],
    "subpilot.sh"
    )
templates = os.path.join(os.path.split(__file__)[0], "templates")

from margit.template import template
from margit.submit import submit
from margit.inspect import inspect
from margit.data import data
from margit.peek import peek

  

## This must remain the last command
from margit.help_func import help; 

