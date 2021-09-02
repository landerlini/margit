import margit 
import os.path
import yaml

__DEFAULT = {
    'JobName': 'MargitJob',
    'Executable': margit.subpilot,
    'LogLevel': 'info',
    'InputSandBox': [],
    'OutputSandBox': [],
    'Setup': "",
    'Command': '{argument}'
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
