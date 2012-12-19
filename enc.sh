#!/bin/bash

SW_SYNC_PATH="/opt/puppet/spacewalk-enc"

## Do no edit below this line

cd $SW_SYNC_PATH
python $SW_SYNC_PATH/src/spacewalk-puppet-enc.py $1
exit $?
