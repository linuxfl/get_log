import os
import re
import string
import sys
import json

def process(bid_in,win_in,click_in,shitu_out):
    win_set = set()
    for raw_line in open(win_in):
        line = raw_line.lower().rstrip("\r\n").strip().split("|")
        req_id = line[1]
        win_set.add(req_id)

    click_set = set()
    for raw_line in open(click_in):
        line = raw_line.lower().rstrip("\r\n").strip().split("|")
        click_set.add(line[1])

#    download_set = set()
#    for raw_line in open(down_in):
#        line = raw_line.lower().rstrip("\r\n").strip().split("|")
#        download_set.add(line[1])

    fp_w = open(shitu_out,"w")

    for raw_line in open(bid_in):
        line = raw_line.lower().rstrip("\r\n").strip().split("\001")
        auction = line[0].split("\t")[-1]
        if auction not in win_set:
    #        print "no auction[%s] in win! "%(auction)
            continue
        click_label = 0
        if auction in click_set:
            click_label = 1
#        download_label = 0
#        if auction in download_set:
#            download_label = 1
        fp_w.write("%d\001%s\n"%(click_label,raw_line.replace("\t","\001").rstrip("\r\n")));
#        fp2_w.write("%d\001%s\n"%(download_label,raw_line.replace("\t","\001").rstrip("\r\n")));

    fp_w.close()

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print "Usage %s bid_log win_events click_event shitu_log"%(sys.argv[0])
        sys.exit(1)
    process(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
