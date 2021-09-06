# margit
Named after Margit Wigner, wife of Paul Dirac, this package wish to make it easier to interact with LHCb Dirac

> As usual, Margit and Hofer chatted convivially while the 
  frail Dirac sat motionless in his favourite old chair, occasionally looking 
  through the glass sliding doors of the garden. For the first half an hour or 
  so of the conversation, he was, as usual, mute but came vibrantly to life when
  Margit happened to mention his distant French ancestors. Dirac corrected one of 
  Margit historical's facts and began to speak [...] talking fluently in his quiet,
  clear voice. 

From *The Strangest Man: The Hidden Life of Paul Dirac, Quantum Genius*, by G. Farmelo. 

### Example 
Let's start with an hello world

```bash 
 # Ensure the envionment is setup
 lb-dirac
 lhcb-proxy-init

 # Install margit
 $ pip install --user git+https://github.com/landerlini/margit

 # Update PATH (in principle not necessary, but lb-dirac environment likes it)
 $ export PATH=$HOME/.local/bin:$PATH

 # Define the job
 $ echo "ls -lrt" > test.sh

 # Submit the two copied from test.sh as jobs
 $ margit submit -n 2 test.sh > test.job

 # Inspect the status of the job
 $ margit inspect test.job

 # Peek the stdout of test.sh as run remotely
 $ margit peek test.job 
```

### Template
Some templated configuration can be used for more 
advanced usages, for example, here is an example 
for sending a job requiring tensorflow2

```bash 
 # Create your python file
 $ nano script.py

 # Launch the script through dirac using the tensorflow template
 $ margit submit -t tensorflow script.py > test.job
```

The environment can be customized, by cloning an existing 
template and modifying the library versions and similars
```bash 
 # Get the template 
 $ margit template tensorflow > mytensorflow.template

 # Edit the configuration of the libraries
 $ nano mytensorflow.template

 # Launch the script through dirac using the modified template
 $ margit submit -t mytensorflow.template script.py > test.job
```

To list the available default templates
```bash
 $ margit template ls
```

To know more about one of the templates
```bash
 $ margit template <template_name> --docs
```


### Integrating with DAG tools (such as snakemake)
A brutal approach to integrate Dirac with DAG tools is to create idling jobs
on the local machine that simply wait for the remote job to end to download 
the output as if it was their own. 
This approach makes it possible to combine local and remote jobs, for example 
data reduction can be offloaded to Dirac while the training of some 
machine learning algorithm can be performed locally using hardware accelerators. 

In order to let margit wait for Dirac to complete, and then downloading its 
output you can issue the following command
```
 $ margit submit [-t ...] script.py \
    --input \
    <path_file1>:<file1_name_in_sandbox> \
    [<path_file2>:<file2_name_in_sandbox> ...] \
    --output \ 
    <output_file1_in_sandbox>:<local_filepath> \
    [<output_file2_in_sandbox>:<local_filepath> ...]
```
if you wish you can also specify a timeout in seconds through the `--wait`
argument. 

For example, the following command
```
 $ margit submit helloworld.sh -i /tmp/myfile.dat:input.txt -o output.txt:/tmp/output.dat -w 3600
```
submits the script helloworld through DIRAC, it copies an inputs text file
from the local `tmp` folder to the remote job through the sandbox, waits up to 
one hour for the job to be accepted and finish and finally it, upon success, it copies
the job output file `output.txt` back to the local `tmp`, modifying the extension to `dat`. 

Using this interface you can configure snakemake (or other tools) to wait for the output 
file to be generated in a specific location before passing it as an input to some subsequent
job.







# Limitations and known bugs
`margit` is NOT a replacement for ganga. 

`margit` ignores everything related to data management, especially for what 
concerns input data. 
Indeed, `margit` is intended to ease the usage of Dirac for HPC jobs where data 
can be accessed remotely because data access (network) is expected to represent
a negligible fraction of the computational cost. 
For HTC applications of the grid, plase use ganga. 

The installation of `conda` fails on several Computing Elements because uneven
environment configuration. We currently restrict submissions to CNAF.

Setup and in general, distribution, is incomplete.
