import margit 
import os.path
import yaml

import string
import random

__DEFAULT = {
    'JobName': 'MargitJob',
    'Executable': margit.subpilot,
    'LogLevel': 'info',
    'InputSandBox': ['{argument}'],
    'OutputSandBox': [],
    'Setup': "",
    'Command': './{argument}',
    'RequireExecutable': True,
    'Options': {},
    'OutputData': [],
}


def get_template (tname):
    template = __DEFAULT.copy()
    ## Custom Template
    if tname is not None and os.path.isfile (tname):
      with open(tname) as f:
          template.update(yaml.load(f, Loader=yaml.SafeLoader))
    ## Default template
    elif tname is not None and os.path.isfile(os.path.join(margit.templates, f"{tname}.template")):
      with open(os.path.join(margit.templates, f"{tname}.template")) as f:
          template.update(yaml.load(f, Loader=yaml.SafeLoader))
    ## Empty template
    elif tname is None:
      pass
    else:
      raise RuntimeError (f"Unexpected template definition {tname}")

    return template


def get_random_string (length=12):
  chars = string.ascii_letters + string.digits
  return "".join([random.choice(chars) for i in range(8)])
