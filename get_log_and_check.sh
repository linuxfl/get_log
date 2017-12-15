#!/bin/bash

bash -x get_log.sh
if [[ $? -ne 0 ]];then
    python dingding_notifier.py "get log error!!!"
    exit 1
fi
