import numpy as np 
import time

import subprocess

__dirac = None

def get_dirac ():
  global __dirac
  if __dirac is None:
    from DIRAC.Core.Base.Script import parseCommandLine
    #from LHCbDIRAC.Interfaces.API.DiracLHCb import DiracLHCb
    #__dirac = DiracLHCb()
    from DIRAC.Interfaces.API.Dirac import Dirac
    __dirac = Dirac()

  return __dirac 

def get_job ():
  from LHCbDIRAC.Interfaces.API.LHCbJob import LHCbJob
  return LHCbJob() 

