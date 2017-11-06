#--coding:utf-8-- 
import os
import re
import string
import sys
import json

def process(infile,outfile):
# {"app_id":1,"augments":{"100000339":{"freq_adid":64,"freq_cid":8},"100000340":{"freq_adid":64,"freq_cid":52},"100000341":{"freq_adid":64,"freq_cid":4},"total":64},"cpc_id":1,"cpm_id":1,"cpx_id":1,"ctr_id":2,"ext":"{\"native_adtype\":8,\"provider\":\"dmssp\"}\n","h5_id":1,"load_id":1,"native_info":"{\"image\":[{\"height\":144,\"image_type\":101,\"image_url\":\"https://jupiterbucket2.oss-cn-hangzhou.aliyuncs.com/HZDM%2Fcreative%2F1000145%2F58097ff33a73b.jpg\",\"width\":144},{\"height\":330,\"image_type\":301,\"image_url\":\"https://jupiterbucket2.oss-cn-hangzhou.aliyuncs.com/HZDM%2Fcreative%2F1000145%2F5809935d4db29.jpg\",\"width\":640}],\"native_config_id\":8,\"word\":[{\"content\":\"网络办卡\",\"length\":20,\"word_type\":1},{\"content\":\"一天拿卡\",\"length\":22,\"word_type\":2}]}\n","pctr":"0.007076","pcvr":"0.000000","pload":"0.000000","wap":0}
    fp_w = open(outfile,"w")
    click_dict = {}

    for raw_line in open(infile):
        line = raw_line.lower().rstrip("\r\n").split("\001")
        
        affname = line[47].strip()
        offerid = line[45].strip()

        key = affname + "\001" + offerid
        country_code = line[26].strip().split(":")[0].upper()
        
        if key in click_dict:
            if country_code in click_dict[key]:
                click_dict[key][country_code] += 1
            else:
                click_dict[key][country_code] = 1
        else:
            click_dict[key] = {}
            click_dict[key][country_code] = 1

    for key,value in click_dict.items():
        
        keys = key.strip().split("\001")
        affname = keys[0]
        offerid = keys[1]

        for k,v in value.items():
            if v < 100:
                del(value[k])
            else:
                value[k] = value[k] * 1.0 / 1000

        fp_w.write("%s,%s,\"{"%(affname,offerid))
        ecpm_str = ""
        for k,v in value.items():
            ecpm_str += "\"\"%s\"\":%s,"%(k,v)
        ecpm_str = ecpm_str.rstrip(",")
        fp_w.write(ecpm_str)
        #fp_w.write(json.dumps(value))
        fp_w.write("}\"\n")

    fp_w.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage %s infile outfile"%(sys.argv[0])
        sys.exit(1)
    process(sys.argv[1],sys.argv[2])
