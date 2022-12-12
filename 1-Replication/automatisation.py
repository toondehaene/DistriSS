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
    #file.close()

def post_normal(filename):
    file = {'file': (r"./testfiles/" + filename, open(r"./testfiles/" + filename, 'rb'), 'application/octet-stream')}
    res = session.post(f'{base_url}/files_mp', data={'storage': 'raid1', 'filename': 'test'}, files=file)
    content = res.content
    id = json.loads(content)["id"]
    print(id)
    # print(dict(res.iter_content))
    #file.close()

    
def scheduling():
    res = session.post(f'{base_url}/start_scheduling', data={})
    print(res.text)
    
def get(fileID):
    res = session.get(f'{base_url}/files/'+str(fileID), data={})
    print(res)
    
    
"""   Tests for post files.
  
df_delegated = pd.DataFrame()
for file in filenames:
    timings = []
    for i in range(100):
        time1 = time.time()
        post_delegated(file)
        time2 = time.time()
        timings.append(time2-time1)
    df_delegated.insert(0,column = str(file), value=timings)
df_delegated.to_csv(r"./testresults/delegated_upload_results.csv")
print("done with delegated uploads")

df_normal = pd.DataFrame()
for file in filenames:
    timings = []
    for i in range(100):
        time1 = time.time()
        post_normal(file)
        time2 = time.time()
        timings.append(time2-time1)
    df_normal.insert(0,column = str(file), value=timings)
df_normal.to_csv(r"./testresults/normal_upload_results.csv")
print("done with normal uploads")
"""
# Tests for get file
#we know that file id 28-127 are 10kb, 128-227 are 100kb, 228-327 are 1mb, 328-427 are 10mb

df_get = pd.DataFrame()
ids = [30, 130, 230, 330]
for id in ids:
    timings = []
    for i in range(100):
        time1 = time.time()
        get(id)
        time2 = time.time()
        timings.append(time2-time1)
    df_get.insert(0,column = str(id), value=timings)
df_get.to_csv(r"./testresults/get_results.csv")
print("done with get")
