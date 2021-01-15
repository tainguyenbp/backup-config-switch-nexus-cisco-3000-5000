#!/bin/bash

# Add the EPEL Repository
sudo yum install epel-release -y

# Install pip 
sudo yum install python-pip -y

# Verify Pip installation
pip --version

# Install development tools 
sudo yum install python-devel -y
sudo yum groupinstall 'development tools' -y

# consider upgrading version pip
pip install --upgrade pip

# pip install a package named requests
pip install requests

# install a package named netmiko
pip install netmiko

# Install pip3
yum install -y python3

# consider upgrading version pip
pip3 install --upgrade pip

# pip3 install a package named requests
pip3 install requests

# pip3 install a package named netmiko
pip3 install netmiko
