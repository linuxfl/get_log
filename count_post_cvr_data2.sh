#!/bin/bash

source functions.sh
conversion_noauth=/home/work/disk/Hive/data/conversion_log/conversion_noauth.log
conversion_auth=/home/work/disk/Hive/data/conversion_log/conversion_auth.log

python count_post_cvr_data.py ${conversion_noauth} con_stat_noauth.dat
if [[ $? -ne 0 ]];then
    echo "cout post cvr data error!"
    exit 1
fi

python count_post_cvr_data.py ${conversion_auth} con_stat_auth.dat
if [[ $? -ne 0 ]];then
    echo "cout pos cvr data error"
    exit 1
fi

scp_model con_stat_noauth.dat "172.16.42.111" "/home/work/run_env/DEPLOY/Hive/Bidder/data" "con_stat_noauth.dat"
scp_model con_stat_noauth.dat "172.16.42.112" "/home/work/run_env/DEPLOY/Hive/Bidder/data" "con_stat_noauth.dat"
scp_model con_stat_auth.dat "172.16.42.111" "/home/work/run_env/DEPLOY/Hive/Bidder/data" "con_stat_auth.dat"
scp_model con_stat_auth.dat "172.16.42.112" "/home/work/run_env/DEPLOY/Hive/Bidder/data" "con_stat_auth.dat"
