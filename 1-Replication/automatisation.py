import sys
import requests
import json
import string
import time
import pandas as pd

base_url = f'http://192.168.0.101:9000'
session = requests.session()
filenames =  ["file"+str(size)+"k.raw" for size in [10_000, 100_000, 1_000_000, 10_000_000]]


def post_delegated(filename):
    #file = open(r"./testfiles/" + filename, mode="rb")  #todo add the file
    file = {'file': (r"./testfiles/" + filename, open(r"./testfiles/" + filename, 'rb'), 'application/octet-stream')}
    res = session.post(f'{base_url}/files_mp_delegated', data={'storage': 'raid1', 'filename': 'test'}, files=file)
    content = res.content
    id = json.loads(content)["id"]
    print(id)
    return json.loads(res.content)
    #file.close()

def post_normal(filename):
    file = {'file': (r"./testfiles/" + filename, open(r"./testfiles/" + filename, 'rb'), 'application/octet-stream')}
    res = session.post(f'{base_url}/files_mp', data={'storage': 'raid1', 'filename': 'test'}, files=file)
    content = res.content
    id = json.loads(content)["id"]
    print(id)
    return json.loads(res.content)

    
def scheduling():
    res = session.post(f'{base_url}/start_scheduling', data={})
    print(res.text)
    
def get(fileID):
    res = session.get(f'{base_url}/files/'+str(fileID), data={})
    print(res)

# index result with ["lead_node_done"] or ["last_node_done"]
def get_server_timing(fileID):
    res = session.get(f'{base_url}/files/'+str(fileID), data={})
    print(res.cookies)
    return json.loads(res.content)
    

"""
df_delegated = pd.DataFrame()
df_leadtiming_delegated = pd.DataFrame()
df_lasttiming_delegated = pd.DataFrame()
for file in filenames:
    timings = []
    leadtimings = []
    lasttimings = []
    for i in range(100):
        time1 = time.time()
        jsonresult = post_delegated(file)
        time2 = time.time()
        timings.append(time2-time1)
        leadtimings.append(float(jsonresult["lead_node_done"]))
        lasttimings.append(float(jsonresult["last_node_done"]))
    df_delegated.insert(0,column = str(file), value=timings)
    df_leadtiming_delegated.insert(0,column = str(file), value=leadtimings)
    df_lasttiming_delegated.insert(0,column = str(file), value=lasttimings)
df_delegated.to_csv(r"./testresults/delegated_upload_results.csv")
df_leadtiming_delegated.to_csv(r"./testresults/delegated_lead_results.csv")
df_lasttiming_delegated.to_csv(r"./testresults/delegated_last_results.csv")

print("done with delegated uploads")
"""

df_normal = pd.DataFrame()
df_leadtiming_normal = pd.DataFrame()
df_lasttiming_normal = pd.DataFrame()
for file in filenames:
    timings = []
    leadtimings = []
    lasttimings = []
    for i in range(100):
        time1 = time.time()
        jsonresult = post_normal(file)
        print(jsonresult)
        time2 = time.time()
        timings.append(time2-time1)
        leadtimings.append(float(jsonresult["lead_node_done"]))
        lasttimings.append(float(jsonresult["last_node_done"]))
    df_normal.insert(0,column = str(file), value=timings)
    df_leadtiming_normal.insert(0,column = str(file), value=leadtimings)
    df_lasttiming_normal.insert(0,column = str(file), value=lasttimings)
df_normal.to_csv(r"./testresults/normal_upload_results.csv")
df_leadtiming_normal.to_csv(r"./testresults/normal_lead_results.csv")
df_lasttiming_normal.to_csv(r"./testresults/normal_last_results.csv")

# Tests for get file
#we know that file id 28-127 are 10kb, 128-227 are 100kb, 228-327 are 1mb, 328-427 are 10mb
"""
doesnt make sense with json bye

df_get = pd.DataFrame()
df_leadtiming = pd.DataFrame()
df_lasttiming = pd.DataFrame()
ids = [30, 130, 230, 330]
for id in ids:
    timings = []
    leadtimings = []
    lasttimings = []
    for i in range(100):
        time1 = time.time()
        jsonresult = get_server_timing(id)
        time2 = time.time()
        timings.append(time2-time1)
        leadtimings.append(float(jsonresult["lead_node_done"]))
        lasttimings.append(float(jsonresult["last_node_done"]))
    df_get.insert(0,column = str(id), value=timings)
    df_leadtiming.insert(0,column = str(id), value=leadtimings)
    df_lasttiming.insert(0,column = str(id), value=lasttimings)
df_get.to_csv(r"./testresults/get_results.csv")
df_leadtiming.to_csv(r"./testresults/lead_get_results.csv")
df_lasttiming.to_csv(r"./testresults/last_get_results.csv")
print("done with get")
"""