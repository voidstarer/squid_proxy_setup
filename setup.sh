#!/usr/bin/env bash

apt-get update
apt-get -y upgrade
echo iptables-persistent iptables-persistent/autosave_v4 boolean true | sudo debconf-set-selections
echo iptables-persistent iptables-persistent/autosave_v4 boolean true | sudo debconf-set-selections
echo iptables-persistent iptables-persistent/autosave_v6 boolean true | sudo debconf-set-selections

apt-get -y install iptables-persistent git

echo "Doing my task.."
# get the repo to install and set-up
git clone https://github.com/light-bringer/python-shell
cd python-shell
python setup.py

# after setup is done, uninstall git and cleanup
echo "Cleaning UP..."
apt-get -y remove git
cd ..
rm -rf python-shell
echo "Done......!"
