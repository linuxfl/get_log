#!/bin/bash
source ./functions.sh
file_time_flag=$(date -d "-1 hour"  +%Y%m%d%H)
active_time_flag=$(date -d "-1 hour"  +%Y-%m-%d_%H)
current_time_flag=$(date -d "-0 hour"  +%Y-%m-%d_%H)
echo $file_time_flag

current_path=$(cd "$(dirname "$0")"; pwd)

done_file_path="/home/work/disk/Hive/done_path"
done_file=${done_file_path}/action_auth.done
source ${done_file}

incre_click=auth_incre_click_${file_time_flag}
new_end_time_stamp=${end_timestamp}
last_end_time_stamp=${end_timestamp}
:>${incre_click}

# ~/disk/Hive/data/clicked_shitu_log
for file in `ls  /home/work/disk/Hive/data/clicked_shitu_log/click_shitu_auth_[0-9]* | tac`;do
    timeflag=${file:0-10}
    if (( timeflag > last_end_time_stamp ));then
        cat ${file}  >> ${incre_click}
        if (( timeflag > new_end_time_stamp ));then
            new_end_time_stamp=${timeflag}
        fi  
    else
        break
    fi  
done

python process_install_num_auth.py ${incre_click} ${incre_click}.tag
if [[ $? -ne 0 ]];then
    echo "process install num error"
    exit 1
fi

add_line=`sed -n "$=" ${incre_click}`
cat ${incre_click}.tag >> ${click_log} &&  rm -rf ${incre_click} && rm -rf ${incre_click}.tag

fix_sample_number=1
if [[ $fix_sample_number -eq 1 ]];then
    if [[ $add_line -ne 0 ]];then
        sed -i "1,${add_line}d" ${click_log}
    fi
fi

mv ${conversion_log} ${conversion_log}.bk
python join_action.py ${click_log} ${active_events_log} ${conversion_log}
if [[ $? -ne 0 ]];then
    echo "join action error!"
    exit 1
fi

cp ${done_file} ${done_file}.bk
echo "end_timestamp=${new_end_time_stamp}" > ${done_file}
echo "click_log=${click_log}" >> ${done_file}
echo "conversion_log=${conversion_log}" >> ${done_file}
echo "active_events_log=${active_events_log}" >> ${done_file}

exit 0
