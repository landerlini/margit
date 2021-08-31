import sys 
from functools import wraps

import margit.core

cli_commands = {}

def cli_command (f):
  global cli_commands 
  cli_commands [f.__name__] = f


from margit.template import template
from margit.submit import submit
from margit.inspect import inspect
from margit.peek import peek

  

## This must remain the last command
from margit.help_func import help; 

