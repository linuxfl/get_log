#!/bin/bash 
source ./functions.sh
python process_offer_click.py /home/work/disk/Hive/data/clicked_shitu_log/batch_click_shitu cooee_ecpm_info_tmp.csv

scp_model cooee_ecpm_info_tmp.csv "172.16.42.111" "/home/work/run_env/DEPLOY/Hive/Router/conf" "cooee_ecpm_info_tmp.csv"
