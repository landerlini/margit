#!/bin/bash 

SETUP=$1
COMMAND=$2
export MARGITJOBID=$3


(IFS=';'; for setupline in $SETUP; do eval $setupline; done) 

`echo $COMMAND`

