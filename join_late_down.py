import os
import re
import string
import sys
import json
def process(inclick,inshitu,outshitu):
    click_set = set()
    for raw_line in open(inclick):
        line = raw_line.lower().rstrip("\r\n").strip().split("|")
        if line[2]  == "download":
            click_set.add(line[1])
    ##inshitu
    fp_w = open(outshitu,"w")
    for raw_line in open(inshitu):
        line = raw_line.lower().rstrip("\r\n").strip().split("\001")
        label = int(line[0])
        auction = line[3]
        if label == 1:
            fp_w.write(raw_line)
            continue
        if auction in click_set:
            print "hit late download[%s]!"%(auction)
            label = 1
        fp_w.write("%d\001%s\n"%(label,"\001".join(raw_line.rstrip("\r\n").split("\001")[1:])))

    fp_w.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage %s event_file down_log_ori down_log_final"%(sys.argv[0])
        sys.exit(1)
    process(sys.argv[1],sys.argv[2],sys.argv[3])
