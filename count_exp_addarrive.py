#duser!/usr/bin/env python 
import sys
import math
import operator
import json
'''
0^A1^ABID^A2017-Apr-18 08:00:00.39664^Ac34d92fbde5dcae2da16be5759160698^A10000265^A2017-04-18 16:00:00^Acooee_hive^Acooee_hive^A^A100131^ALanzador fresco^A^A^Acom.cool.launcher^A358392018923770^A358392018923770^A358392018923770^A358392018923770^A73211^Ajinchangtai^AP7^AAndroid^A4.4.2^A1^A2^A4.4:46999:0:others^ACO:CO:-:-::-1:-1^Ahttp://com.cool.launcher/^A181.143.13.242^A^A8^A2^A32701105^A{1,1.000000}^A0^Alocal^A{"bid_id":1,"ctr_id":1,"ext":"{\"applist\":[\"com.google.android.apps.photos\",\"com.fundevs.app.mediaconverter\",\"com.whatsapp\",\"com.wsandroid.suite\",\"devian.tubemate.home\"],\"provider\":\"cooee_hive\"}\n","native_info":"{\"image\":null,\"native_config_id\":-1,\"word\":null}\n","pctr":"0.467076","pcvr":"0.000000","posterName":"NoPoster","spot_format":"720x1280"}^A218346061^A^A0x0^A0^A0^A^A^A0.420000^A11574666^A0^Amobi^Acom.playrix.fishdomdd.gplay^A1.000000^A1.000000CNY^ACHN^A^A^A^A
'''
if len(sys.argv) < 2:
    print help
coutn_file = open(sys.argv[1], 'r')

total = 0
pos_num = 0
neg_num = 0
total_price = 0
total_action = 0
total_action_click = 0

creative_dict = {}
exchange_dict = {}
traffic_dict={}
bundle_dict = {}
ad_dict = {}
total_dict = {}
country_dict={}
offer_dict={}
authority_dict={}
for line in coutn_file:
    fleds = line.strip().split("\001")
#    if len(fleds) <49:
#        continue

    label = int(fleds[1])
    if label != 1:
        label = 0
    if label == 0:
        neg_num = neg_num + 1
    else:
        pos_num = pos_num + 1

    active_label = label
    total_action_click += active_label
    
    try:
        exp_dict = json.loads(fleds[37])
    except:
        print "format[%s] not json[%s]"%(fleds[37],fleds[4])
        print line
        continue

    price = fleds[45]
    try:
        price_num = float(price)
    except:
        continue

    action = int(fleds[0])
    total_action += action
    if action != 1:
        price_num = 0
    total_price = total_price + price_num 
   
    if not isinstance(exp_dict, dict):
        continue
    for key,value in exp_dict.items():
        if "ext" in exp_dict:
            try:
                ext = json.loads(exp_dict["ext"])
            except:
                continue
        else:
            continue

        install_authority = 0
        if "install_authority" in ext:
            install_authority = int(ext["install_authority"])
        else:
            continue

        if install_authority == 1:
            if key.find("_id")  == -1:
                continue
            if "noauth" in key:
                continue
        else:
            if key.find("_id") == -1:
                continue
            if "noauth" not in key:
                continue
        
        key_str = "%s_%s"%(key,value)
#        key_str = fleds[46] 
        #total_dict["%s_%d"%(key,value)] = {}
        sub_dict = {"show":0,"clk":0,"price":0,"load":0,"action":0,"action_clk":0}

        if key_str in total_dict:
            sub_dict = total_dict[key_str]
        sub_dict["show"]+=1
        sub_dict["clk"]+=label
        sub_dict["action_clk"]+=active_label
        sub_dict["price"]+=price_num
        sub_dict["action"]+=action
        total_dict[key_str] = sub_dict
        
        sub_dict = {"show":0,"clk":0,"price":0,"load":0,"action":0,"action_clk":0,"newshow":0,"newclk":0,"newprice":0,"newload":0,"newaction":0,"newaction_clk":0}

        if key_str in offer_dict:
            sub_dict = offer_dict[key_str]
        if fleds[50] != "1.000000":
            sub_dict["show"]+=1
            sub_dict["clk"]+=label
            sub_dict["action_clk"]+=active_label
            sub_dict["price"]+=price_num
            sub_dict["action"]+=action
        else:
            sub_dict["newshow"]+=1
            sub_dict["newclk"]+=label
            sub_dict["newaction_clk"]+=active_label
            sub_dict["newprice"]+=price_num
            sub_dict["newaction"]+=action
        offer_dict[key_str] = sub_dict
        
        sub_dict = {"show":0,"clk":0,"price":0,"load":0,"action":0,"action_clk":0,"cost":0,"noauthshow":0,"noauthclk":0,"noauthprice":0,"noauthload":0,"noauthaction":0,"noauthaction_clk":0,"noauthcost":0}
        try:
            ext = json.loads(exp_dict["ext"])
        except:
            continue
        if "install_authority" not in ext:
            continue
        install_auth = int(ext["install_authority"])

        if key_str in authority_dict:
            sub_dict = authority_dict[key_str]
        if install_auth == 1:
            sub_dict["show"]+=1
            sub_dict["clk"]+=label
            sub_dict["action_clk"]+=active_label
            sub_dict["price"]+=price_num
            sub_dict["action"]+=action
        else:
            sub_dict["noauthshow"]+=1
            sub_dict["noauthclk"]+=label
            sub_dict["noauthaction_clk"]+=active_label
            sub_dict["noauthprice"]+=price_num
            sub_dict["noauthaction"]+=action
        authority_dict[key_str] = sub_dict

    country = fleds[27].split(":")[0]
    sub_dict = {"show":0,"clk":0,"price":0,"load":0,"action":0,"action_clk":0,"cost":0}
    if country in country_dict:
        sub_dict = country_dict[country]
    sub_dict["show"]+=1
    sub_dict["clk"]+=label
    sub_dict["price"]+=price_num
    sub_dict["action"]+=action
    sub_dict["action_clk"]+=active_label
    country_dict[country] = sub_dict
    sub_dict = {"show":0,"clk":0,"price":0,"load":0,"action":0,"action_clk":0,"cost":0}
'''
    sub_dict = {"show":0,"clk":0,"price":0,"load":0,"action":0,"action_clk":0,"cost":0}
    if bundle in bundle_dict:
        sub_dict = bundle_dict[bundle]
    sub_dict["show"]+=1
    sub_dict["clk"]+=label
    sub_dict["cost"]+=price_num
    sub_dict["action_clk"]+=active_label
    sub_dict["action"]+=action
    bundle_dict[bundle] = sub_dict
'''
coutn_file.close()

total = neg_num + pos_num
cpm = (total_price*1000) / total
pos_rate = (0.0 + pos_num) / total
cvr = 0.0
if total_action_click > 0:
    cvr = float(total_action)/total_action_click
print("Total  SHOW:%10d, CLICK:%5d CTR:%5f ACTION:%5d CVR:%5f INCOME:%5f CPM:%5f" % (total,pos_num,pos_rate,total_action,cvr,total_price,cpm))

for k,v in sorted(total_dict.items(),cmp=lambda x,y : cmp(x[0], y[0]),reverse=False):
    click = float(v["clk"])
    show = float(v["show"])
    load = float(v["load"])
    action = float(v["action"])
    action_click = float(v["action_clk"])
    income = float(v["price"])
    cpm = (income) / (show) * 1000
    ctr = (click) / ((show) + 0.0)
    action_r = 0.0
    if action_click > 0:
        action_r = (action)/float(action_click)
    print("%s Model SHOW:%10d, CLICK:%7d CTR:%5f Conversion:%5d CVR:%5f INCOME:%5f CPM:%5f" % (k,show, click, ctr, action,action_r,income,cpm))
for k,v in sorted(offer_dict.items(),cmp=lambda x,y : cmp(x[0], y[0]),reverse=False):
    click = float(v["clk"])
    show = float(v["show"])
    load = float(v["load"])
    action = float(v["action"])
    action_click = float(v["action_clk"])
    income = float(v["price"])
    cpm = (income) / (show) * 1000
    ctr = (click) / ((show) + 0.0)
    action_r = 0.0
    if action_click > 0:
        action_r = (action)/float(action_click)
    print("Old Offer %s Model SHOW:%10d, CLICK:%7d CTR:%10f ACTION:%10d ACTION_CLICK:%10d CVR:%f CPM:%f" % (k,show, click, ctr, action,action_click,action_r,cpm))
    
    click = float(v["newclk"])
    show = float(v["newshow"])
    load = float(v["newload"])
    action = float(v["newaction"])
    action_click = float(v["newaction_clk"])
    income = float(v["newprice"])
    cpm = (income) / (show) * 1000
    ctr = (click) / ((show) + 0.0)
    action_r = 0.0
    if action_click > 0:
        action_r = (action)/float(action_click)
    print("New Offer %s Model SHOW:%10d, CLICK:%7d CTR:%10f ACTION:%10d ACTION_CLICK:%10d CVR:%f CPM:%f" % (k,show, click, ctr, action,action_click,action_r,cpm))

'''for k,v in sorted(authority_dict.items(),cmp=lambda x,y : cmp(x[0], y[0]),reverse=False):
    click = float(v["clk"])
    show = float(v["show"])
    load = float(v["load"])
    action = float(v["action"])
    action_click = float(v["action_clk"])
    income = float(v["price"])
    cpm = (income) / (show) * 1000
    ctr = (click) / ((show) + 0.0)
    action_r = 0.0
    if action_click > 0:
        action_r = (action)/float(action_click)
    print("Has Authority %s Model SHOW:%10d, CLICK:%7d CTR:%10f ACTION:%10d ACTION_CLICK:%10d CVR:%f CPM:%f" % (k,show, click, ctr, action,action_click,action_r,cpm))
    
    click = float(v["noauthclk"])
    show = float(v["noauthshow"])
    load = float(v["noauthload"])
    action = float(v["noauthaction"])
    action_click = float(v["noauthaction_clk"])
    income = float(v["noauthprice"])
    cpm = (income) / (show) * 1000
    ctr = (click) / ((show) + 0.0)
    action_r = 0.0
    if action_click > 0:
        action_r = (action)/float(action_click)
    print("No  Authority %s Model SHOW:%10d, CLICK:%7d CTR:%10f ACTION:%10d ACTION_CLICK:%10d CVR:%f CPM:%f" % (k,show, click, ctr, action,action_click,action_r,cpm))
'''
'''
print("Country,Show,Click,CTR,Conversion,income,cpm")
for k,v in sorted(country_dict.items(),cmp=lambda x,y : cmp(x[0], y[0]),reverse=False):
    click = float(v["clk"])
    show = float(v["show"])
    load = float(v["load"])
    action = float(v["action"])
    action_click = float(v["action_clk"])
    income = float(v["price"])
    cpm = income / show * 1000
    ctr = click / (show + 0.0)
    action_r = 0.0
    if action_click > 0:
        action_r = action/float(action_click)
    print("%s,%d,%d,%f,%d,%f,%f" % (k,show, click, ctr, action,income,cpm))
'''
'''
for k,v in sorted(creative_dict.items(),cmp=lambda x,y : cmp(x[0], y[0]),reverse=False):
    click = float(v["clk"])
    show = float(v["show"])
    load = float(v["load"])
    action = float(v["action"])
    action_click = float(v["action_clk"])
    income = float(v["price"])
    cpm = income / show * 1000
    ctr = click / (show + 0.0)
    action_r = 0.0
    if action_click > 0:
        action_r = action/float(action_click)
    print("%s Model  SHOW:%10d, CLICK:%7d CTR:%10f ACTION:%10d ACTION_CLICK:%10d CVR:%f CPM:%f" % (k,show, click, ctr, action,action_click,action_r,cpm))
'''
