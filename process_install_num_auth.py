#--coding:utf-8-- 
import os
import re
import string
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def process(infile,outfile):
# {"app_id":1,"augments":{"100000339":{"freq_adid":64,"freq_cid":8},"100000340":{"freq_adid":64,"freq_cid":52},"100000341":{"freq_adid":64,"freq_cid":4},"total":64},"cpc_id":1,"cpm_id":1,"cpx_id":1,"ctr_id":2,"ext":"{\"native_adtype\":8,\"provider\":\"dmssp\"}\n","h5_id":1,"load_id":1,"native_info":"{\"image\":[{\"height\":144,\"image_type\":101,\"image_url\":\"https://jupiterbucket2.oss-cn-hangzhou.aliyuncs.com/HZDM%2Fcreative%2F1000145%2F58097ff33a73b.jpg\",\"width\":144},{\"height\":330,\"image_type\":301,\"image_url\":\"https://jupiterbucket2.oss-cn-hangzhou.aliyuncs.com/HZDM%2Fcreative%2F1000145%2F5809935d4db29.jpg\",\"width\":640}],\"native_config_id\":8,\"word\":[{\"content\":\"网络办卡\",\"length\":20,\"word_type\":1},{\"content\":\"一天拿卡\",\"length\":22,\"word_type\":2}]}\n","pctr":"0.007076","pcvr":"0.000000","pload":"0.000000","wap":0}
    fp_w = open(outfile,"w")
    for raw_line in open(infile):
        line = raw_line.lower().rstrip("\r\n").split("\001")
        try:
            meta_info = json.loads(line[36])
            ext = meta_info["ext"] 
        except:
            continue

        try:
            applist = json.loads(ext)["applist"]
            installnum = len(applist)
        except:
#            print raw_line;
            installnum = 0
        isnew = 0
        if line[49] == "1.000000":
            isnew = 1
        
        try:
            diffclk = int(meta_info["offer_country_click_2h"]) - int(meta_info["offer_country_click_1h"])
            diffconv = int(meta_info["offer_country_conversion_2h"]) - int(meta_info["offer_country_conversion_1h"])
            fp_w.write("%s\001%s\001%s\001%s\001%s\001%s\001%s\001%s\001%s\n"%(raw_line.rstrip("\r\n"),"insnum"+str(installnum),str(isnew),meta_info["offer_country_click"],meta_info["offer_country_conversion"],diffclk,diffconv,meta_info["offer_country_click_1h"],meta_info["offer_country_conversion_1h"]));
        except:
            fp_w.write("%s\001%s\001%s\001%s\001%s\001%s\001%s\001%s\001%s\n"%(raw_line.rstrip("\r\n"),"insnum"+str(installnum),str(isnew),"0","0","0","0","0","0"));
    fp_w.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage %s infile outfile"%(sys.argv[0])
        sys.exit(1)
    process(sys.argv[1],sys.argv[2])
