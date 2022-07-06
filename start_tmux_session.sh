#!/bin/sh

if [ "$#" -ne 1 ]; then
	echo "Please specify a config file"; exit 1
fi

CONFIG_FILE=$(readlink -f $1)

echo $CONFIG_FILE

# Set Session Name
SESSION="bec"
SESSIONEXISTS=$(tmux list-sessions | grep $SESSION)


tmux new-session -d -s $SESSION

tmux rename-window -t 0 'Main'
tmux send-keys -t 'Main' "source ./bec/bec_venv/bin/activate; cd ./bec/koss; python launch.py --config $CONFIG_FILE" C-b-m

tmux split-window -h
tmux split-window -h
tmux select-layout even-horizontal

tmux select-pane -t 1
tmux send-keys -t 'Main' "source ./bec/bec_venv/bin/activate; cd ./bec/opaas; python launch.py --config $CONFIG_FILE" C-b-m

tmux select-pane -t 2
tmux send-keys -t 'Main' "source ./bec/bec_venv/bin/activate; cd ./bec/scan_bundler; python launch.py --config $CONFIG_FILE" C-b-m

#tmux send-keys -t 'Main' C-b-% C-b-m

#tmux new-window -t $SESSION:1 -n 'OPAAS'
#tmux send-keys -t 'OPAAS' 'cd bluekafka/opaas' C-m 'ls' C-m

#tmux attach-session -t $SESSION
