#--coding:utf-8-- 
import os
import re
import string
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def process(infile,outfile,flag):
# {"app_id":1,"augments":{"100000339":{"freq_adid":64,"freq_cid":8},"100000340":{"freq_adid":64,"freq_cid":52},"100000341":{"freq_adid":64,"freq_cid":4},"total":64},"cpc_id":1,"cpm_id":1,"cpx_id":1,"ctr_id":2,"ext":"{\"native_adtype\":8,\"provider\":\"dmssp\"}\n","h5_id":1,"load_id":1,"native_info":"{\"image\":[{\"height\":144,\"image_type\":101,\"image_url\":\"https://jupiterbucket2.oss-cn-hangzhou.aliyuncs.com/HZDM%2Fcreative%2F1000145%2F58097ff33a73b.jpg\",\"width\":144},{\"height\":330,\"image_type\":301,\"image_url\":\"https://jupiterbucket2.oss-cn-hangzhou.aliyuncs.com/HZDM%2Fcreative%2F1000145%2F5809935d4db29.jpg\",\"width\":640}],\"native_config_id\":8,\"word\":[{\"content\":\"网络办卡\",\"length\":20,\"word_type\":1},{\"content\":\"一天拿卡\",\"length\":22,\"word_type\":2}]}\n","pctr":"0.007076","pcvr":"0.000000","pload":"0.000000","wap":0}
    fp_w = open(outfile,"w")
    for raw_line in open(infile):
        line = raw_line.lower().rstrip("\r\n").split("\001")
        try:
            meta_info = json.loads(line[36])
            ext = json.loads(meta_info["ext"])
        except:
            continue
        #try:
        if int(ext["install_authority"]) == flag:
            fp_w.write(raw_line);
        #except:
        #    print raw_line
        #    fp_w.write("%s\001%s\n"%(raw_line.rstrip("\r\n"),0));
    fp_w.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage %s infile outfile"%(sys.argv[0])
        sys.exit(1)
    process(sys.argv[1],sys.argv[2],int(sys.argv[3]))
