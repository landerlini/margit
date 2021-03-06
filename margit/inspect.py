import time 
from datetime import datetime

import margit
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
    parser.add_argument("--timeout",  "-t", default=5, type=int, help="Time waited before timeout error (seconds)")

    dirac = margit.core.get_dirac()

    args = parser.parse_args(args)

    for fname in args.jobdesc:
      with open(fname) as f:
        j = yaml.load(f, Loader=yaml.SafeLoader)

      if 'JobID' not in j.keys():
        print (f"Warning: {fname} does not seem a submission token", file=sys.stderr)
        continue
      
      start = datetime.now()
      statuses = dict()
      while 'Value' not in statuses.keys():
        statuses = dirac.getJobStatus(j['JobID'])

        if (datetime.now() - start).seconds > args.timeout:
          raise RuntimeError(f"LHCbDirac job not available. {str(statuses)}" )

        if 'Value' not in statuses.keys():  # Often the reason of the error is dirac 
          time.sleep(0.1)                    # in a partially initialized state

      for key, entry in statuses['Value'].items():
        print (f"{j['JobName']:20s} | {key:10d} | {entry['Site']:20s} | {entry['Status']:10s} | {entry['MinorStatus']}")

    

      

