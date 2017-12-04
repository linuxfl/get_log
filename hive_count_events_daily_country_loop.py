import os
import json
import time
import subprocess

class HiveEventsCount:
    def __init__(self, file_dir, file_name):
        self.file_dir = file_dir
        self.file_name = file_name
        self.events_count = {}
        self.dup_keys = {}
        # (2009, 2, 17, 10, 48, 39, 1, 48, 0)
        self.now = int(time.time())
        self.local_time = time.strftime("%Y%m%d", time.localtime(self.now))
        self.window = 24 * 60 * 60 * 3

    def load_data(self, file_name):
        file_data = open(file_name, "r")
        self.events_count = json.load(file_data)
        file_data.close()

    def save_data(self, file_name):
        output = open(file_name, "w")
        file_data = json.dumps(self.events_count, ensure_ascii=False, sort_keys=True, indent=4)
        output.write(file_data)
        output.close()

    def read_file(self, file_name):
        print "file_name", file_name
        
        file_data = open(file_name, "r")
        for line in file_data:
            split_data = line.strip().split("|")
            if len(split_data) != 11:
                continue
            provider = split_data[0]
            if provider == "cooee":
                provider = "cooee_hive"
            auction_id = split_data[1]
            ev_type = split_data[2]
            aff_name = split_data[7]
            offer_id = split_data[3]
            pay_out = split_data[5]
            country_code = split_data[8]
            install_authority = split_data[9]
            cooee_make = split_data[10]
            access_time = int(float(split_data[6]))

            _type = install_authority
            #if cooee_make.find("hlcy") != -1:
            #    _type = "hlcy"

            key = aff_name + "_" + offer_id
            key2 = auction_id + "_" + ev_type
            
            if access_time + self.window < self.now:
                continue 

            if self.dup_keys.has_key(key2):
                continue
            else:
                self.dup_keys[key2] = 1

            if self.events_count is None:
                self.events_count = {}

            if not self.events_count.has_key(provider):
                self.events_count[provider] = {}
            if not self.events_count[provider].has_key(key):
                self.events_count[provider][key] = {}
            if not self.events_count[provider][key].has_key(country_code):
                self.events_count[provider][key][country_code] = {}

            if not self.events_count[provider][key][country_code].has_key(_type):
                self.events_count[provider][key][country_code][_type] = {
                    "win": 0,
                    "click": 0,
                    "refer": 0,
                    "refer_error": 0,
                    "download": 0,
                    "install": 0,
                    "active": 0,
                    "conversion": 0,
                    "income": 0
                }
            try:
                self.events_count[provider][key][country_code][_type][ev_type] += 1
            except:
                print "error", line

            if ev_type == "conversion":
                self.events_count[provider][key][country_code][_type]["income"] += float(pay_out)

    def generate_events(self):
        today_log = self.file_dir + "events.log"

        self.read_file(today_log)
            
        self.save_data(self.file_dir + self.file_name)

if __name__ == "__main__":
    hec = HiveEventsCount("./", "hive_events_count_daily_country_3d.json")
    hec.generate_events()
    exit(0)
    while True:
        print "********** start counting **********"
        start = time.time()
        print start
        hec = HiveEventsCount("./", "hive_events_count_daily_country.json")
        hec.generate_events()
        child2 = subprocess.Popen(["./scp_day_file_hive.sh"], stdout=subprocess.PIPE)
        out = child2.communicate()
        end = time.time()
        print end-start
        time.sleep(1)





