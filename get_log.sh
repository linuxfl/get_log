#!/bin/bash
file_time_flag=$(date -d "-1 hour"  +%Y%m%d%H)
pre_file_time_flag=$(date -d "-2 hour"  +%Y%m%d%H)
current_time_flag=$(date +%Y%m%d%H)
#today_flag=$(date -d "-1 day"  +%Y%m%d)
today_flag=$(date -d "-0 day"  +%Y%m%d)

echo $file_time_flag

pid=$$
#engine log
remote_log_machine=172.16.42.112
remote_log_path=/home/work/run_env/DEPLOY/Hive/Logger/log
HOME="/home/work/disk/Hive/data"
dest_file_path="${HOME}/ori_log"
bid_path="${dest_file_path}/bid_log"
[[ ! -d ${bid_path} ]] && mkdir -p ${bid_path}

#event log
remote_event_machine=172.16.42.109
remote_event_path=/home/work/run_env/DEPLOY/events_server/release/logs
event_path="${dest_file_path}/event_log"
[[ ! -d ${event_path} ]] && mkdir ${event_path}

shitu_path="${HOME}/shitu_log"
[[ ! -d ${shitu_path} ]] && mkdir ${shitu_path}

download_path="${HOME}/shitu_download_log"
[[ ! -d ${download_path} ]] && mkdir ${download_path}

current_path=$(cd "$(dirname "$0")"; pwd)
done_file_path=${HOME}/done_path

if [ ! -d $done_file_path ]; then
	mkdir $done_file_path
fi

done_file=${done_file_path}/shitu.done.${file_time_flag}
[[ -f ${done_file} ]] && echo "${done_file} exit " && exit 0

touch ${done_file}
#active.
bid_file=bid.$file_time_flag.log
#event_file=events.$file_time_flag.log
event_file=events.log
event_file2=events.log.${today_flag}

echo "get bid log form machine"
scp -l 50000 work@$remote_log_machine:$remote_log_path/$bid_file ${bid_path}

echo "get events log from machine"
scp -l 50000 work@$remote_event_machine:$remote_event_path/${event_file} ${event_path}
#scp -l 20000 work@$remote_event_machine:$remote_event_path/${event_file2} ${event_path}

echo "get file done"
done_file_time_flag=$(date -d "-1 hour"  +%Y%m%d%H)
done_file_pretime_flag=$(date -d "-2 hour"  +%Y%m%d%H)

rm -rf $shitu_path/shitu_${done_file_time_flag}

win_path="${dest_file_path}/win_event_log"
[[ ! -d ${win_path} ]] && mkdir ${win_path}
click_path="${dest_file_path}/click_event_log"
[[ ! -d ${click_path} ]] && mkdir ${click_path}
active_path="${dest_file_path}/active_event_log"
[[ ! -d ${active_path} ]] && mkdir ${active_path}

gawk -F'|'  '$3=="win"' ${event_path}/${event_file2}  > ${win_path}/win.${file_time_flag}.log
gawk -F'|'  '$3=="click"' ${event_path}/${event_file2}  > ${click_path}/click.${file_time_flag}.log
#gawk -F'|'  '$3=="download"' ${event_path}/${event_file2}  > ${click_path}/download.${file_time_flag}.log
gawk -F'|'  '$3=="win"' ${event_path}/${event_file}  >> ${win_path}/win.${file_time_flag}.log
gawk -F'|'  '$3=="click"' ${event_path}/${event_file}  >> ${click_path}/click.${file_time_flag}.log
#gawk -F'|'  '$3=="download"' ${event_path}/${event_file}  >> ${click_path}/download.${file_time_flag}.log
gawk -F'|'  '$3=="conversion"' ${event_path}/${event_file}  >> ${active_path}/conversion_events.batch.log

current_hour=$(date -d "-0 day"  +%H)
if [[ "$current_hour"x = "01"x ]];then
    scp -l 20000 work@$remote_event_machine:$remote_event_path/${event_file2} ${event_path}
    gawk -F'|'  '$3=="conversion"' ${event_path}/${event_file2}  >> ${active_path}/conversion_events.batch.log
fi

cp ${active_path}/conversion_events.batch.log ${active_path}/conversion_events.batch.log.bak
sort ${active_path}/conversion_events.batch.log.bak | uniq > ${active_path}/conversion_events.batch.log

python join_win_click.py ${bid_path}/bid.${done_file_time_flag}.log ${win_path}/win.${file_time_flag}.log ${click_path}/click.${file_time_flag}.log  ${shitu_path}/shitu_$done_file_time_flag 
if [[ $? -ne 0 ]];then
    echo "join shitu log error"
    exit 1
fi

shitu_addlate_path="/home/work/disk/Hive/data/shitu_log_addlateclick"

python join_late_click.py ${click_path}/click.${file_time_flag}.log ${shitu_path}/shitu_${pre_file_time_flag} ${shitu_addlate_path}/shitu_${pre_file_time_flag} 
if [[ $? -ne 0 ]];then
    echo "join late click log error"
    exit 1
fi

#shitu_addlate_down_path="/home/work/disk/Hive/data/shitu_log_addlatedown"

#python join_late_down.py ${click_path}/download.${file_time_flag}.log ${download_path}/shitu_download_${pre_file_time_flag} ${shitu_addlate_down_path}/shitu_download_${pre_file_time_flag} 
#if [[ $? -ne 0 ]];then
#    echo "join late down log error"
#    exit 1
#fi

#pre3_file_time_flag=$(date -d "-3 hour"  +%Y%m%d%H)
#python join_late_down.py ${click_path}/download.${file_time_flag}.log ${download_path}/shitu_download_${pre3_file_time_flag} ${shitu_addlate_down_path}/shitu_download_${pre3_file_time_flag}_late3 
#if [[ $? -ne 0 ]];then
#    echo "join late down log error"
#    exit 1
#fi

pos_shitu_path="${HOME}/clicked_shitu_log"
[[ ! -d ${pos_shitu_path} ]] && mkdir ${pos_shitu_path}
#pos_download_shitu_path="${HOME}/downloaded_shitu_log"
#[[ ! -d ${pos_download_shitu_path} ]] && mkdir ${pos_download_shitu_path}

gawk -F'\001' '$1==1' ${shitu_path}/shitu_$done_file_time_flag > ${pos_shitu_path}/click_shitu_$done_file_time_flag

#seperate the install authority and no install authority click log
python process_install_authority.py ${pos_shitu_path}/click_shitu_$done_file_time_flag ${pos_shitu_path}/click_shitu_auth_$done_file_time_flag 1
python process_install_authority.py ${pos_shitu_path}/click_shitu_$done_file_time_flag ${pos_shitu_path}/click_shitu_noauth_$done_file_time_flag 0

#gawk -F'\001' '$1==1' ${download_path}/shitu_download_$done_file_time_flag > ${pos_download_shitu_path}/download_shitu_$done_file_time_flag
#scp action
exit 0
