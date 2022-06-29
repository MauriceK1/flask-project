#!/bin/sh

cd /root/flask-project/

git fetch --all
git pull

source python3-virtualenv/bin/activate
pip install -r requirements.txt

sudo systemctl restart myportfolio