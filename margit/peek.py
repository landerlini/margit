import margit
import datetime
from argparse import ArgumentParser
import yaml

import os
import os.path
import sys 

from glob import glob


@margit.cli_command
def peek(args):
    "Retrieve the output sandbox from a file and displays its stdout"
    parser = ArgumentParser(usage="margit inspect <arguments>")
    parser.add_argument("jobdesc", nargs='+', help="Executable file to submit")
    parser.add_argument("--outputdir", "-o", help="Scratch dir for the output", default='.')

    args = parser.parse_args(args)

    for fname in args.jobdesc:
      with open(fname) as f:
        j = yaml.load(f, Loader=yaml.SafeLoader)

      if 'JobID' not in j.keys():
        print (f"Warning: {fname} does not seem a submission token", file=sys.stderr)
        continue
      
      for jobid in j['JobID']:
        margit.core.get_dirac().getOutputSandbox(jobid, outputDir=args.outputdir)
        with open(os.path.join(args.outputdir, f"{jobid}/Script1_{os.path.basename(j['Executable'])}.log")) as stdout:
          print (stdout.read())

    

      

