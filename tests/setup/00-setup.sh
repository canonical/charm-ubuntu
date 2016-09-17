#!/bin/bash -x

# Install amulet if not already installed.
dpkg -s amulet
if [ $? -ne 0 ]; then
    sudo add-apt-repository -y ppa:juju/stable
    sudo apt-get update -qq
    sudo apt-get install -y amulet
fi
