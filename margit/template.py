import margit 
from argparse import ArgumentParser 
from margit.utils import get_template
import yaml 

import os
import os.path 

from glob import glob

def template_docs ():
  "Internal. Return the documentation of the defined templates"
  template_files = glob(os.path.join(margit.templates, '*.template'))
  docs = []
  for fname in template_files:
    template = os.path.split(fname)[1]
    if template.startswith('.'): continue 
    title = template[:-len('.template')]
    t = get_template(fname)
    docstr = ""
    if 'Docs' in t.keys(): docstr = t['Docs'].split("\n")[0][:64]
    docs.append (f"{title:15s} {docstr:64s}")

  return "\n".join(docs)

@margit.cli_command
def template (args):
  "Create a template for a DIRAC job"
  parser = ArgumentParser (usage="margit template <arguments>")
  parser.add_argument ("template", help = "Default template to clone", default=margit.subpilot)
  parser.add_argument ("--name", "-n", default = "MargitJob", help = "Job name")
  parser.add_argument ("--inputSB", "-i", nargs = '+', default = [], help = "List of files to send to the input sandbox")
  parser.add_argument ("--outputSB", "-o", nargs = '+', default = [], help = "List of files to retrieve through to the output sandbox")
  parser.add_argument ("--settings", "-s", nargs = '+', default = [], help = "List of bash scripts to copy the settings from")
  parser.add_argument ("--verbose", "-v", action='store_true', help = "Enhance job verbosity to ease debug")
  parser.add_argument ("--docs", "-d", action='store_true', help="Display the docs of the selected template and exits")

  args = parser.parse_args (args) 

  if args.template == 'ls':
    print(template_docs())
    exit() 

   
  template = get_template (args.template) 

  if args.docs:
    print (f"\nDocumentation for template: {args.template.upper()}\n  ", 
        template['Docs'] if 'Docs' in template.keys() else "Docs not available"
        )
    return 

  inputSB = sum([glob(f) for f in args.inputSB], template['InputSandBox'])

  settings = []
  for fname in args.settings:
    with open(fname) as f:
      lines = f.read().split("\n")
      settings += [l for l in lines if len(l) and l[:2] != "#!"]

  template.update(dict(
      JobName = args.name, 
      LogLevel = 'verbose' if args.verbose else 'info', 
      InputSandBox  = inputSB,
      OutputSandBox = args.outputSB,
      Setup = settings
    )
  )

  print (yaml.dump(template)) #, default_style='|') )






