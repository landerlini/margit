import margit
import datetime
from argparse import ArgumentParser
import yaml

import os
import os.path

from glob import glob

__DEFAULT = {
    'JobName': 'MargitJob',
    'Executable': None,
    'LogLevel': 'info',
    'InputSandBox': [],
    'OutputSandBox': []
}


@margit.cli_command
def submit(args):
    "Makes a job out of a template and submit it"
    parser = ArgumentParser(usage="margit template <arguments>")
    parser.add_argument("template", help="Executable file to submit")
    parser.add_argument("--njobs", "-n", default=1, help="Number of jobs to submit", type=int)
    parser.add_argument("--local", "-L", action='store_true',
                        help="Submit the job to local")

    args = parser.parse_args(args)

    template = __DEFAULT.copy()
    with open(args.template) as f:
        template.update(yaml.load(f, Loader=yaml.SafeLoader))

    print ("### DO NOT EDIT THIS FILE ###")
    print(yaml.dump(template))
    job = margit.core.get_job()
    job.setName(template['JobName'])
    job.setExecutable(template['Executable'])
    job.setLogLevel(template['LogLevel'])

    if len(template['InputSandBox']):
        job.setInputSandbox(template['InputSandBox'])

    if len(template['OutputSandBox']):
        job.setOutputSandbox(template['OutputSandBox'])

    if args.local:
        job.runLocal(margit.core.get_dirac())
        return
    
    ids = []
    for iJob in range(args.njobs):
      ids.append ( margit.core.get_dirac().submitJob(job) ['JobID'] )

    print ("#"*80)
    print (yaml.dump({
      'JobID': ids,
      'submission': str(datetime.datetime.now())
      }))

