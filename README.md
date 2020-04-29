# cloudify-benchmark-tool
A tool used to create and install deployments based on uploaded rest-blueprint

# rest-server configuration

install rest-server on a centos host using :

``` bash configure.sh ```

then to run the server ``` python app.py ```

this will start the server on port 5000

# Configure Environemnt to use the tool

-- to make sure that pip works , you have to
```
sudo yum update -y || sudo apt-get update -y
sudo yum install -y epel-release || true
sudo yum install -y python-pip || sudo apt-get install python-pip -y
sudo yum groupinstall -y "Development Tools" || true
sudo yum install -y python-devel || sudo apt-get install python-dev -y
```
-- then install python requirments
```
pip install -r requirements.txt
```


# Blueprint upload to manager
to upload the blueprint that will be used by this tool :


then :
```
python uploadBlueprint.py --config-path config.yaml --blueprint-path [path_to_blueprint_yaml_file] --blueprint-name [name of blueprint]
```

# Running the tool
to start running the tool :
```
python CBT.py --config-path config.yaml --blueprint-name [name of blueprint] --deployments-count [number of deployments to create & install] --max-threads-count [number of parallel executions to run on manager]
```
