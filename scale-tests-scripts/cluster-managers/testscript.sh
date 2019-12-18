#!/bin/bash

runtime="60 minute"
endtime=$(date -ud "$runtime" +%s)

while [[ $(date -u +%s) -le $endtime ]]
do
    timeout_val="$[$[$endtime-$(date -u +%s)]/60]"
    if [ $timeout_val -le 0 ]
      then
        exit 0
    fi
    timeout_val="${timeout_val}m"
    echo $timeout_val
    timeout $timeout_val python $1 --config-path config.yaml --max-threads-count 12
done
