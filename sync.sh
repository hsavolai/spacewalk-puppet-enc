#!/bin/bash

SW_SYNC_PATH="/opt/puppet/spacewalk-enc"

SPACEWALK_USERNAME="spacewalk-user"
SPACEWALK_PASSWORD=""

# RPC API URL (i.e. https://spacewalk/rpc/api")
SPACEWALK_URL="https://server.example.com/rpc/api"

## Do no edit below this line

cd $SW_SYNC_PATH
python $SW_SYNC_PATH/src/spacewalk-puppet-sync.py -u $SPACEWALK_USERNAME -p $SPACEWALK_PASSWORD -s $SPACEWALK_URL $1

