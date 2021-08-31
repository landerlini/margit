import margit 


@margit.cli_command
def help(args):
  "Print this help and exits"
  for fname, fobj in margit.cli_commands.items():
    print (f"{fname:15s} {fobj.__doc__:40s}")
