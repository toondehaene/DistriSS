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
    return None
    
    
    
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
# all_averages_delegated = []

# for filename in filenames:
#     average = []
#     for i in range(100):
#         time1 = time.time()
#         post_delegated(filename)
#         time2 = time.time()
#         average.append(time2-time1)
#     average.sort()
#     average = average[5:95]
#     average = sum(average) / len(average)
#     all_averages_delegated.append(average)
   
# print("Post delegated results : 10k, 100k, 1Mb, 10Mb") 
# print(all_averages_delegated)

# all_averages_normal = []

# for filename in filenames:
#     average = []
#     for i in range(100):
#         time1 = time.time()
#         post_normal(filename)
#         time2 = time.time()
#         average.append(time2-time1)
#     average.sort()
#     average = average[5:95]
#     average = sum(average) / len(average)
#     all_averages_normal.append(average)

print("Post normal results : 10k, 100k, 1Mb, 10Mb") 
# print(all_averages_normal)