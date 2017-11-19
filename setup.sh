#!/usr/bin/env bash


echo iptables-persistent iptables-persistent/autosave_v4 boolean true | sudo debconf-set-selections
echo iptables-persistent iptables-persistent/autosave_v4 boolean true | sudo debconf-set-selections

sudo apt-get -y install iptables-persistent

python setup.py
