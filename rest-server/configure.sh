sudo yum update -y || sudo apt-get update -y
sudo yum install -y epel-release || true
sudo yum install -y python-pip || sudo apt-get install python-pip -y
sudo pip install flask flask-restful
