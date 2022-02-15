import time 
from datetime import datetime

import margit
from argparse import ArgumentParser
import yaml

import os
import os.path
import sys 
import json

from glob import glob


@margit.cli_command
def data(args):
    "Retrieve from DIRAC the status of one or more jobs"
    parser = ArgumentParser(usage="margit inspect <arguments>")
    parser.add_argument("jobdesc", nargs='+', help="Executable file to submit")
    parser.add_argument("--timeout",  "-t", default=5, type=int, help="Time waited before timeout error (seconds)")
    formats = ['inout.json', 'in.json', 'out.json', 'in.txt', 'out.txt']
    parser.add_argument("--format",  "-f", choices=formats, default='out.txt', help="Time waited before timeout error (seconds)")

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

      what, how = args.format.split('.')

      input_lfns = []
      output_lfns = []

      for key, entry in statuses['Value'].items():
        if entry['Status'].lower() == 'done':
          if 'in' in what:
            try: 
              inputs = dirac.getJobInputData(key)
              input_lfns += [(key, v) for v in inputs['Value']]
            except KeyError as e:
              print (f"Input of job {key} cannot be retrieved" , file=sys.stderr)
              

          if 'out' in what:
            try: 
              outputs = dirac.getJobOutputData(key)
              output_lfns += [(key, v) for v in outputs['Value']]
            except KeyError as e:
              print (f"Output of job {key} cannot be retrieved" , file=sys.stderr)
      

      if what == 'inout':
        if how == 'json':
          print (json.dump(dict(
            Inputs=[v for _,v in input_lfns], 
            Outputs=[v for _,v in output_lfns], 
            )))
      elif what == 'in':
        if how == 'json':
          print (json.dump(dict(
            Inputs=[v for _,v in input_lfns], 
            )))
        elif how == 'txt':
          print ("\n".join ([v for _,v in input_lfns]))
      elif what == 'out':
        if how == 'json':
          print (json.dump(dict(
            Inputs=[v for _,v in output_lfns], 
            )))
        elif how == 'txt':
          print ("\n".join ([v for _,v in output_lfns]))

      

    

      


