# cloudify-benchmark-tool
A tool used to create and install deployments based on uploaded rest-blueprint

# rest-server configuration
install rest-server on a centos host using : 
``` bash configure.sh ```
then to run the server ``` python app.py ```
this will start the server on port 5000

# Blueprint upload to manager
to upload the blueprint that will be used by this tool :
-- first we have to install python requirments 
``` pip install -r requirements.txt ```
then :
``` python uploadBlueprint.py --config-path config.yaml --blueprint-name [name of blueprint] ```

# Running the tool
to start running the tool :
``` python CBT.py --config-path config.yaml --blueprint-name [name of blueprint] --deployments-count [number of deployments to create & install] --max-threads-count [number of parallel executions to run on manager ```
