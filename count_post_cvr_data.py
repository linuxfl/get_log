#!/usr/bin/env python 
import sys
import math
import operator

fp_conv_w = open(sys.argv[2],"w")
coutn_file = open(sys.argv[1], 'r')
conv_dict = {}

for line in coutn_file:
    fleds = line.strip().split("\001")
    con_label = int(fleds[0])
    click_label = int(fleds[1])
    media_name = fleds[11]

    coutry = fleds[27]
    coutry = coutry.strip().split(":")[0]
    offer_id = fleds[46] 
    aff_name = fleds[48]
    price_num = float(fleds[45]) 

    key_str = "%s_%s"%(offer_id,aff_name) 
    #key_str = "%s_%s_%s"%(coutry,offer_id,aff_name)
    sub_dict = {"clk":0,"action":0,"income":0.0}
    if key_str in conv_dict:
        sub_dict = conv_dict[key_str]
    sub_dict["clk"]+=click_label
    sub_dict["action"]+=con_label
    if con_label == 1:
        sub_dict["income"]+=price_num
    conv_dict[key_str] = sub_dict

for k,v in sorted(conv_dict.items(),cmp=lambda x,y : cmp(x[0], y[0]),reverse=False):
    click_num = float(v["clk"])
    con_num = float(v["action"])
    price_num = float(v["income"])
    fp_conv_w.write("%s %d %d %f\n" % (k,click_num,con_num,price_num))
