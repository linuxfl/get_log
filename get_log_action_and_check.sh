#!/bin/bash
if [[ $# -ne 1 ]];then
    echo "Usage:cmd auth/noauth"
    exit 1
fi

if [[ $1 == "auth" ]];then
    bash -x get_log_action_auth.sh
    if [[ $? -ne 0 ]];then
        python dingding_notifier.py "get log action auth error!!!"
        exit 1
    fi
elif [[ $1 == "noath" ]];then
    bash -x get_log_action_noauth.sh
    if [[ $? -ne 0 ]];then
        python dingding_notifier.py "get log action noauth error!!!"
        exit 1
    fi
else
    echo "error parameter!"
    exit 1
fi
exit 0
