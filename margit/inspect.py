import margit
import datetime
from argparse import ArgumentParser
import yaml

import os
import os.path
import sys 

from glob import glob


@margit.cli_command
def inspect(args):
    "Retrieve from DIRAC the status of one or more jobs"
    parser = ArgumentParser(usage="margit inspect <arguments>")
    parser.add_argument("jobdesc", nargs='+', help="Executable file to submit")

    args = parser.parse_args(args)

    for fname in args.jobdesc:
      with open(fname) as f:
        j = yaml.load(f, Loader=yaml.SafeLoader)

      if 'JobID' not in j.keys():
        print (f"Warning: {fname} does not seem a submission token", file=sys.stderr)
        continue
      
      for key, entry in margit.core.get_dirac().getJobStatus(j['JobID'])['Value'].items():
        print (f"{j['JobName']:20s} | {key:10d} | {entry['Site']:20s} | {entry['Status']:10s} | {entry['MinorStatus']}")

    

      

