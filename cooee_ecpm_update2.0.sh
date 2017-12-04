#!/bin/bash

source functions.sh

events_log="events.log"
time_windows=2
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

python hive_count_events_daily_country_loop.py 

rm ${events_log}
scp_model hive_events_count_daily_country_3d.json "172.16.42.111" "/home/work/run_env/DEPLOY/Hive/Router/conf" "hive_events_count_daily_country_3d.json"
scp_model hive_events_count_daily_country_3d.json "172.16.42.112" "/home/work/run_env/DEPLOY/Hive/Router/conf" "hive_events_count_daily_country_3d.json"
