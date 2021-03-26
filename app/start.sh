#!/usr/bin/env bash

# install aws cli
# curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
# unzip awscliv2.zip
# ./aws/install

# apt-get install -y less

# curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.17.12/2020-11-02/bin/linux/amd64/kubectl
# chmod +x ./kubectl

# aws eks --region eu-west-1 update-kubeconfig --name central
export PATH=/miniconda/bin:$PATH
echo ". /miniconda3/etc/profile.d/conda.sh" >> ~/.profile
conda init bash
eval "$(conda shell.bash hook)"
export PYTHONPATH=/env/bin/python
ls
ls ..
conda activate /env
service nginx start
uwsgi --ini uwsgi.ini