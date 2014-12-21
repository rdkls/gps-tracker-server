#!/bin/bash
SESSION_NAME=gps_serve

tmux has-session -t ${SESSION_NAME} 2>/dev/null
if [ $? != 0 ] ; then
    tmux new-session -s ${SESSION_NAME} -d

    tmux send-keys -t ${SESSION_NAME} 'cd ~/ws/gps/www' C-m
    tmux send-keys -t ${SESSION_NAME} 'python -m SimpleHTTPServer 9898' C-m

    tmux split-window -t ${SESSION_NAME}
    tmux send-keys -t ${SESSION_NAME} 'cd ~/ws/gps' C-m
    tmux send-keys -t ${SESSION_NAME} '. venv/gps/bin/activate' C-m
    tmux send-keys -t ${SESSION_NAME} './rest_api/rest_api.py' C-m

    tmux split-window -t ${SESSION_NAME}
    tmux send-keys -t ${SESSION_NAME} 'cd ~/ws/gps/www' C-m
    tmux send-keys -t ${SESSION_NAME} 'gulp watch' C-m

fi
tmux attach -t ${SESSION_NAME}
