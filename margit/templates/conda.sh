#!/bin/sh
export HOME=`pwd`
python3 -m site --user-site

touch $HOME/.bashrc
echo "SHELL: $SHELL"


curl https://repo.anaconda.com/miniconda/Miniconda3-py38_4.10.3-Linux-x86_64.sh -o conda_installer.sh
STATUS=`echo "935d72deb16e42739d69644977290395561b7a6db059b316958d97939e9bdf3d conda_installer.sh" | sha256sum -c`
if [[ $STATUS == *OK* ]] 
then
  echo "download verified"
  chmod +x conda_installer.sh
fi

./conda_installer.sh -b
if [[ $SHELL == *bash* ]] 
then
  $HOME/miniconda3/bin/conda init bash
  source $HOME/.bashrc
else
  $HOME/miniconda3/bin/conda init bash
  source $HOME/.bashrc
fi

echo "Running Miniconda3, version `conda -V`" >> output.log

SETUP=$1
COMMAND=$2

(IFS=';'; for setupline in $SETUP; do eval $setupline; done) 

`echo $COMMAND`
