# margit
Named after Margit Wigner, wife of Paul Dirac, this package wish to make it easier to interact with LHCb Dirac

### Example 
```bash 
 # Define the job
 $ echo "ls -lrt" > test.sh

 # Create the job template
 $ margit template test.sh > test.template

 # Submit the two copied from this template as jobs
 $ margit submit test.template -n 2 > test.job

 # Inspect the status of the job
 $ margit inspect test.job

 # Peek the stdout of test.sh as run remotely
 $ margit peek test.job 

```
