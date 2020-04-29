# cluster managers test case

if you are here make sure that you have the environment configured

fill you environment setup fields in `config.yaml`

scripts to use :

* `CBT.py` : this will create and install deployments from an already uploaded blueprint given its `blueprint-name`
* `execute_workflow.py` : this will execute a given workflow on a list of deployment that is in a file called `deployments.txt` inside the same directory with the script [workflows like (`install`, `install_nodes`)]
* `execute_deployments.py` : this will execute a custom operation that we have in the associated blueprint on one node of the deployments that are in a file called `deployments.txt` inside the same directory
* `execute2_deployments.py` : this will execute a custom operation that we have in the associated blueprint on two nodes of the deployments that are in a file called `deployments.txt` inside the same directory
