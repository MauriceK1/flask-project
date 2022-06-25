#!/bin/sh

cd ~/

pkill -f tmux
cd flask-project
git fetch && git reset origin/main --hard


tmux new-session -d -s site
tmux send-keys source\  python3-virtualenv/bin/activate ENTER
tmux send-keys pip \ install\  -r requirements.txt ENTER
tmux send-keys flask \ run \ --host=0.0.0.0 ENTER