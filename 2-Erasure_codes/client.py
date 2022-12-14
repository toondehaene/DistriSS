import requests
import json
import time
import pandas as pd
import argparse

base_url = "http://192.168.0.101:9000/" # TODO: Change address
session = requests.session()
filenames =  ["file"+str(size)+"k.raw" for size in [10_000, 100_000, 1_000_000, 10_000_000]]

def main():
    # Run with number of erasures 1 without delegation
    # Run with number of erasures 2 without delegation
    # Run with number of erasures 1 with delegation
    # Run with number of erasures 2 with delegation

    # parser = argparse.ArgumentParser(description = 'Run program :)')
    # parser.add_argument('-e', '--erasures', type=int, default=1)
    # parser.add_argument('-m', '--measurements', type=int, default=1)
    # args = parser.parse_args()

    print("Starting POST measurement collection...")
    #results = save_file("file10000k.raw", max_erasures=1)
    results = get_file(1)
    print(results)

    # # IDs to do GET measurements on
    # file_ids = []

    # # Dataframes
    # df_client_post = pd.DataFrame()
    # df_full_enc = pd.DataFrame()
    # df_pure_enc = pd.DataFrame()
    # df_lead_done = pd.DataFrame()
    # df_last_done = pd.DataFrame()

    # for file in filenames:
    #     get_file_id = True

    #     client_post_times = []
    #     full_enc_times = []
    #     pure_enc_times = []
    #     lead_done_times = []
    #     last_done_times = []

    #     for i in range(args.measurements):

    #         results = save_file(file, max_erasures=args.erasures)

    #         client_post_times.append(results.get("client_post_time"))
    #         full_enc_times.append(results.get("full_enc_time"))
    #         pure_enc_times.append(results.get("pure_enc_time"))
    #         lead_done_times.append(results.get("lead_done_time"))
    #         last_done_times.append(results.get("last_done_time"))

    #         # Getting only one ID of a file to do GET measurements on
    #         if get_file_id:
    #             file_ids.append(results.get("file_id"))
    #             get_file_id = False

    #     df_client_post.insert(0, column=str(file), value=client_post_times)
    #     df_full_enc.insert(0, column=str(file), value=full_enc_times)
    #     df_pure_enc.insert(0, column=str(file), value=pure_enc_times)
    #     df_lead_done.insert(0, column=str(file), value=lead_done_times)
    #     df_last_done.insert(0, column=str(file), value=last_done_times)

    # # TODO: Change the names when running with delegation.
    # df_client_post.to_csv("./testresults/client_post_results_me" + str(args.erasures) + ".csv")
    # df_full_enc.to_csv("./testresults/full_enc_results_me" + str(args.erasures) + ".csv")
    # df_pure_enc.to_csv("./testresults/pure_enc_results_me" + str(args.erasures) + ".csv")
    # df_lead_done.to_csv("./testresults/lead_results_me" + str(args.erasures) + ".csv")
    # df_last_done.to_csv("./testresults/last_results_me" + str(args.erasures) + ".csv")
    # print("POST measurement done.")

    # print("Starting GET measurement collection...")
    # # file_ids = [42, 45, 48, 51] # Hardcoded for testing

    # # Dataframes
    # df_client_get = pd.DataFrame()
    # df_full_dec = pd.DataFrame()
    # df_pure_dec = pd.DataFrame()

    # for file_id in file_ids:
    #     client_get_times = []
    #     full_dec_times = []
    #     pure_dec_times = []

    #     for i in range(args.measurements):
    #         results = get_file(file_id)

    #         client_get_times.append(results.get("client_get_time"))
    #         full_dec_times.append(results.get("full_dec_time"))
    #         pure_dec_times.append(results.get("pure_dec_time"))

    #     df_client_get.insert(0, column=str(file_id), value=client_get_times) # file_id should be file?
    #     df_full_dec.insert(0, column=str(file_id), value=full_dec_times)
    #     df_pure_dec.insert(0, column=str(file_id), value=pure_dec_times)

    # # TODO: Change the names when running with delegation.
    # df_client_get.to_csv("./testresults/client_get_results_me" + str(args.erasures) + ".csv")
    # df_full_dec.to_csv("./testresults/full_dec_results_me" + str(args.erasures) + ".csv")
    # df_pure_dec.to_csv("./testresults/pure_dec_results_me" + str(args.erasures) + ".csv")
    # print("GET measurement done.")

    
def save_file(filename, max_erasures):

    files = {
        "file": open(r"./testfiles/" + str(filename), "rb")
    }
        
    request_body = {
        "max_erasures": max_erasures
    }

    time1 = time.time()
    response = session.post(base_url + "files_mp", data=request_body, files=files)
    time2 = time.time()

    response = response.json()

    results = {
        "file_id": response.get("id"),

        "client_post_time": time2-time1,
        "full_enc_time": response.get("full_enc"),
        "pure_enc_time": response.get("pure_enc"),
        "lead_done_time": response.get("lead_done"),
        "last_done_time": response.get("last_done")
    }

    return results


def get_file(file_id):
    time1 = time.time()
    response = session.get(base_url + "files/" + str(file_id))
    time2 = time.time()

    results = {
        "file_id": file_id,

        "client_get_time": time2-time1,
        "full_dec_time": response.headers.get("fullDecTime"),
        "pure_dec_time": response.headers.get("pureDecTime")
    }

    return results


if __name__ == "__main__":
    main()
