import margit 
from argparse import ArgumentParser 

import os
import os.path 

from glob import glob

@margit.cli_command
def template (args):
  "Create a template for a DIRAC job"
  parser = ArgumentParser (usage="margit template <arguments>")
  parser.add_argument ("executable", help = "Executable file to submit")
  parser.add_argument ("--name", "-n", default = "MargitJob", help = "Job name")
  parser.add_argument ("--inputSB", "-i", nargs = '+', default = [], help = "List of files to send to the input sandbox")
  parser.add_argument ("--outputSB", "-o", nargs = '+', default = [], help = "List of files to retrieve through to the output sandbox")
  parser.add_argument ("--verbose", "-v", action='store_true', help = "Enhance job verbosity to ease debug")

  args = parser.parse_args (args) 

  if not os.path.isfile (args.executable):
    raise IOError (f"Executable should be an existing file, {args.executable} is not.") 

  if not os.access (args.executable, os.X_OK):
    raise IOError (f"Please mark {os.path.basename(args.executable)} as executable:\n\
     $ chmod +x {os.path.abspath(args.executable)}") 



  with open (os.path.join (os.path.dirname (__file__), "template.yaml")) as f:
    template = f.read()


  inputSB = sum([glob(f) for f in args.inputSB], [])

  isbstr = '[]'
  if len(inputSB):
    isbstr = "\n" + "\n".join ([f"   - {entry}" for entry in inputSB])

  osbstr = '[]'
  if len(args.outputSB):
    osbstr = '\n' + "\n".join ([f"   - {entry}" for entry in args.outputSB])


  template = (template % (dict(
      jobname = args.name, 
      executable = os.path.abspath (args.executable), 
      logLevel = 'verbose' if args.verbose else 'info', 
      inputSB  = isbstr,
      outputSB = osbstr,
    ))
  )

  print (template)






