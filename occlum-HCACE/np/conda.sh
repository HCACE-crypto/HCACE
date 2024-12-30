#!/bin/bash
set -e
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}"  )" >/dev/null 2>&1 && pwd )"


# Install python and dependencies to specified position
[ -f Miniconda3-latest-Linux-x86_64.sh ] || wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
[ -d miniconda ] || bash ./Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda

echo "source /root/miniconda/etc/profile.d/conda.sh" >> ~/.bashrc
source ~/.bashrc

