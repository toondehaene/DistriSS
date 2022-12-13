import requests
import json
import time

base_url = "http://localhost:9000/"
session = requests.session()
filenames =  ["file"+str(size)+"k.raw" for size in [10_000, 100_000, 1_000_000, 10_000_000]]
max_erasures = [1, 2]
number_of_measurements = 100

def main():
    # TODO: 
    # post 4 files with me1
    # post 4 files with me2
    # get 4 files with me1
    # get 4 files with me2




    file = filenames[0]
    time = save_file(file, 1)
    print(time)
        
    





    # me1_ids = [1,2,3,4] # TODO: Input correct IDs 
    # me2_ids = [5,6,7,8] # TODO: Input correct IDs

    # get_me1_measurements = []
    # get_me2_measurements = []

    # for i in range(len(filenames)):
    #     measurement = get_file(i, number_of_measurements)
    #     get_me1_measurements.append(measurement)


def save_file(filename, max_erasures):

    files = {
        "file": open(r"./testfiles/" + str(filename), "rb")
    }
        
    request_body = {
        "max_erasures": 1
    }
    print(files)
    print(request_body)

    time1 = time.time()
    response = session.post(base_url + "files_mp", data=request_body, files=files)
    #print(response)
    time2 = time.time()

    return time2-time1


def get_file(file_id):    
    time1 = time.time()
    response = session.get(base_url + "files/" + str(file_id))
    time2 = time.time()

    return time2-time1

if __name__ == "__main__":
    main()
