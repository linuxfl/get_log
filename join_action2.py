#--coding:utf-8-- 
import os
import re
import string
import sys
import json

def process(click_in,action_in,action_out):
    action_set = set()
    for raw_line in open(action_in):
        line = raw_line.lower().rstrip("\r\n").strip().split("|")
        if line[2] == "conversion":
            action_set.add(line[1])
    fp_w = open(action_out,"w")
    for raw_line in open(click_in):
        line = raw_line.lower().rstrip("\r\n").strip().split("\001")
        auction = line[3]
        action_label = 0
        if auction in action_set:
            action_label = 1
        fp_w.write("%d\001%s\n"%(action_label,raw_line.replace("\t","\001").rstrip("\r\n")));

    fp_w.close()
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage %s click_log action/refer_events action/refer_log"%(sys.argv[0])
        sys.exit(1)
    process(sys.argv[1],sys.argv[2],sys.argv[3])
