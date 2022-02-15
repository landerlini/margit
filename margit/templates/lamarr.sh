## Steering options
OPTIONFILE=$1
GENEVENTS=$2
shift 2


## Function to rename produced output
function name_output
{
  for f in $1;
  do
    mv $f $2;
  done
}

#### LHCb environment
source /cvmfs/lhcb.cern.ch/lib/LbEnv

#### Lamarr step
GENEVENTS=$GENEVENTS \
RUNNUMBER=$((1000 + $MARGITJOBID)) \
lb-run \
  --use=Gen/DecFiles.v30r69 \
  --platform=x86_64_v2-centos7-gcc10-opt \
  Gauss/v55r3 \
  gaudirun.py $OPTIONFILE

name_output "`find *Lamarr*.xsim`" output.xsim

env
