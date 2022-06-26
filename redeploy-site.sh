#!/bin/sh

cd ~/

git fetch --all
git pull

sudo systemctl restart myportfolio