from argparse import ArgumentParser
import sys 
import margit

def main():
  parser = ArgumentParser (usage = "margit <command>")

  parser.add_argument ("command", help="Command", choices=margit.cli_commands) 

  args = parser.parse_args(sys.argv[1:2])

  margit.cli_commands [args.command] (sys.argv[2:]) 

if __name__ == '__main__':
  main() 

