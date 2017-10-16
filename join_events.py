# Copyright (c) MetaCommunications, Inc. 2003-2005
#
# Distributed under the Boost Software License, Version 1.0. 
# (See accompanying file LICENSE_1_0.txt or copy at 
# http://www.boost.org/LICENSE_1_0.txt)
#--coding:utf-8-- 

import os
import re
import string
import sys
import json


##win
#click 
#download
#refer_get
#refer_success
#refer_failure
#install
#active
#refer_broadcast


g_index_dict = {"win":0,
            "click":1,
            "download":2,
            "refer_get":3,
            "refer_success":4,
            "install":5,
            "active":6,
            "refer_broadcast":7
}




def process(bid_in,event_in,shitu_out,refer_out,con_out):

    #cooee|gkasdfkj|click|12312|23881908528  
    auction_events_dict = {}

    for raw_line in open(event_in):
        line = raw_line.lower().rstrip("\r\n").strip().split("|")
        #source|req_id|ev_type|offer_id|dev
        exchange,req_id,event_type,offer_id,dev = line
        if req_id not in auction_events_dict:
            auction_events_dict[req_id] = [0,0,0,0,0,0,0,0]
        auction_events_dict[req_id][g_index_dict[event_type]] = 1


    fp_shitu_w = open(shitu_out,"w")
    fp_con_w = open(con_out,"w")
    fp_refer_w = open(refer_out,"w")

    for raw_line in open(bid_in):
        line = raw_line.lower().rstrip("\r\n").strip().split("\001")
        auction = "%s_%s"%(line[0].split("\t")[-1],line[1])
        if auction not in auction_events_dict:
            print "no auction[%s] in events! "%(auction)
            continue
        win_label,click_label,down_label,refer_get_label,refer_success_label,install_label,active_label,refer_broad_label = auction_events_dict[auction]
        if win_label == 0:
            continue

        fp_shitu_w.write("%d\001%s\001%s\n"%(click_label,raw_line.replace("\t","\001").rstrip("\r\n")));
        if click_label == 0:
            continue
        fp_refer_w.write("%d\001%d\001%s\001%s\n"%(refer_get_label,click_label,raw_line.replace("\t","\001").rstrip("\r\n")));

        fp_con_w.write("%d\001%d\001%d\001%d\001%d\001%s\001%s\n"%(refer_broad_label,active_label,install_label,refer_success_label,refer_get_label,click_label,raw_line.replace("\t","\001").rstrip("\r\n")));



    fp_w.close()
            

            

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print "Usage %s bid_log event_log shitu_log refer_log conversion_log"%(sys.argv[0])
        sys.exit(1)
    process(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    
