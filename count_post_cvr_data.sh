#!/bin/bash

source functions.sh

events_log="events_log"
time_windows=7
end_time_stamp=`date -d "${time_windows} days ago" +%Y%m%d`

:>${events_log}
for file in `ls  /home/work/disk/Hive/data/ori_log/event_log/events\.log\.[0-9]* | tac`;do
    timeflag=${file:0-8}

    if (( timeflag > end_time_stamp ));then
        cat ${file}  >> ${events_log}
    else
        break
    fi  
done

cat /home/work/disk/Hive/data/ori_log/event_log/events.log >> ${events_log}

python count_post_cvr_data2.py ${events_log} con_stat_auth.dat con_stat_noauth.dat
if [[ $? -ne 0 ]];then
    echo "cout post cvr data error!"
    exit 1
fi

rm ${events_log}

scp_model con_stat_noauth.dat "172.16.42.111" "/home/work/run_env/DEPLOY/Hive/Bidder/data" "con_stat_noauth.dat"
scp_model con_stat_noauth.dat "172.16.42.112" "/home/work/run_env/DEPLOY/Hive/Bidder/data" "con_stat_noauth.dat"
scp_model con_stat_auth.dat "172.16.42.111" "/home/work/run_env/DEPLOY/Hive/Bidder/data" "con_stat_auth.dat"
scp_model con_stat_auth.dat "172.16.42.112" "/home/work/run_env/DEPLOY/Hive/Bidder/data" "con_stat_auth.dat"
