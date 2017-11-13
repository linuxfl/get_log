#!/usr/bin/env python 
import sys
import math
import operator

fp_auth_conv_w = open(sys.argv[2],"w")
fp_noauth_conv_w = open(sys.argv[3],"w")

#events.log
coutn_file = open(sys.argv[1], 'r')
noauth_conv_dict = {}
auth_conv_dict = {}

#cooee|aucid|state|offerid| | | |affname|country|install_authority|cooeemake

for line in coutn_file:
    fleds = line.strip().split("|")
    if len(fleds) < 10:
        continue

    state = fleds[2]
    click_label = 0
    conversion_label = 0
    price_num = 0.0
    if state == "click":
        click_label = 1
    elif state == "conversion":
        conversion_label = 1
        price_num = float(fleds[5])
    else:
        continue
        
    offer_id = fleds[3]
    aff_name = fleds[7]
    
    key_str = "%s_%s"%(offer_id,aff_name)
    sub_dict = {"click":0,"conversion":0,"income":0.0}

    if int(fleds[9]) == 0:
        if key_str in noauth_conv_dict:
            sub_dict = noauth_conv_dict[key_str]
        sub_dict["click"]+=click_label
        sub_dict["conversion"]+=conversion_label
        if conversion_label == 1:
            sub_dict["income"]+=price_num
        noauth_conv_dict[key_str] = sub_dict
    else:
        if key_str in auth_conv_dict:
            sub_dict = auth_conv_dict[key_str]
        sub_dict["click"]+=click_label
        sub_dict["conversion"]+=conversion_label
        if conversion_label == 1:
            sub_dict["income"]+=price_num
        auth_conv_dict[key_str] = sub_dict

for k,v in sorted(noauth_conv_dict.items(),cmp=lambda x,y : cmp(x[0], y[0]),reverse=False):
    click_num = float(v["click"])
    con_num = float(v["conversion"])
    price_num = float(v["income"])
    fp_noauth_conv_w.write("%s %d %d %f\n" % (k,click_num,con_num,price_num))

for k,v in sorted(auth_conv_dict.items(),cmp=lambda x,y : cmp(x[0], y[0]),reverse=False):
    click_num = float(v["click"])
    con_num = float(v["conversion"])
    price_num = float(v["income"])
    fp_auth_conv_w.write("%s %d %d %f\n" % (k,click_num,con_num,price_num))
