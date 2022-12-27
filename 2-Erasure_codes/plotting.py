import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statistics as stats


def main():
    m1_data_path = "testresults/delegation_client_get_results_me1.csv"
    m2_data_path = "testresults/delegation_client_get_results_me2.csv"
    plot_data(m1_data_path, m2_data_path, "Download time with delegation")

    m1_data_path = "testresults/nondelegation_client_get_results_me1.csv"
    m2_data_path = "testresults/nondelegation_client_get_results_me2.csv"
    plot_data(m1_data_path, m2_data_path, "Download time without delegation")

    m1_data_path = "testresults/nondelegation_pure_enc_results_me1.csv"
    m2_data_path = "testresults/nondelegation_pure_enc_results_me2.csv"
    plot_data(m1_data_path, m2_data_path, "Encoding time without delegation")

    m1_data_path = "testresults/nondelegation_pure_dec_results_me1.csv"
    m2_data_path = "testresults/nondelegation_pure_dec_results_me2.csv"
    plot_data(m1_data_path, m2_data_path, "Decoding time without delegation")

    m1_data_path = "testresults/delegation_last_results_me1.csv"
    m2_data_path = "testresults/delegation_last_results_me2.csv"
    plot_data(m1_data_path, m2_data_path, "Last done with delegation")

    m1_data_path = "testresults/nondelegation_last_results_me1.csv"
    m2_data_path = "testresults/nondelegation_last_results_me2.csv"
    plot_data(m1_data_path, m2_data_path, "Last done without delegation")

    plt.show()

def plot_data(m1_data_path, m2_data_path, diagram_title):
    m1_ten_kb, m1_hundred_kb, m1_one_mb, m1_ten_mb = get_data(m1_data_path)
    m2_ten_kb, m2_hundred_kb, m2_one_mb, m2_ten_mb = get_data(m2_data_path)

    # region Some lists contain strings instead of floats
    m1_ten_kb = [float(i) for i in m1_ten_kb]
    m1_hundred_kb = [float(i) for i in m1_hundred_kb]
    m1_one_mb = [float(i) for i in m1_one_mb]
    m1_ten_mb = [float(i) for i in m1_ten_mb]

    m2_ten_kb = [float(i) for i in m2_ten_kb]
    m2_hundred_kb = [float(i) for i in m2_hundred_kb]
    m2_one_mb = [float(i) for i in m2_one_mb]
    m2_ten_mb = [float(i) for i in m2_ten_mb]
    # endregion
    
    fig, axs = plt.subplots(2, 2, sharex=False) # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html
    fig.suptitle(diagram_title, fontsize=15)
    
    for ax in axs.flat:
        ax.set(xlabel='Seconds', ylabel='Count')

    for ax in axs.flat:
        ax.label_outer()

    # region 10 kB
    axs[0, 0].hist([m1_ten_kb, m2_ten_kb], density=False, bins=25, rwidth=0.8, label=["L1", "L2"])  # density=False would make counts

    ten_kb_mean = stats.mean(m1_ten_kb + m2_ten_kb)
    ten_kb_median = stats.median(m1_ten_kb + m2_ten_kb)

    # TODO: plot total mean and median or??
    axs[0, 0].axvline(ten_kb_mean, color='k', linestyle='-', linewidth=1, label="Avg.: " + str(round(ten_kb_mean, 4)))
    axs[0, 0].axvline(ten_kb_median, color='k', linestyle='--', linewidth=1, label="Med.: " + str(round(ten_kb_median, 4)))

    axs[0, 0].set_title('10 kB')
    axs[0, 0].legend(loc="upper right")
    axs[0, 0].xaxis.set_tick_params(labelbottom=True)
    # endregion

    # region 100 kB
    axs[0, 1].hist([m1_hundred_kb, m2_hundred_kb], density=False, bins=25, rwidth=0.8, label=["L1", "L2"])

    hundred_kb_mean = stats.mean(m1_hundred_kb + m2_hundred_kb)
    hundred_kb_median = stats.median(m1_hundred_kb + m2_hundred_kb)

    axs[0, 1].axvline(hundred_kb_mean, color='k', linestyle='-', linewidth=1, label="Avg.: " + str(round(hundred_kb_mean, 4)))
    axs[0, 1].axvline(hundred_kb_median, color='k', linestyle='--', linewidth=1, label="Med.: " + str(round(hundred_kb_median, 4)))

    axs[0, 1].set_title('100 kB')
    axs[0, 1].legend(loc="upper right")
    axs[0, 1].xaxis.set_tick_params(labelbottom=True)
    axs[0, 1].yaxis.set_tick_params(labelbottom=True)
    # endregion

    # region 1 MB
    axs[1, 0].hist([m1_one_mb, m2_one_mb], density=False, bins=25, rwidth=0.8, label=["L1", "L2"])

    one_mb_mean = stats.mean(m1_one_mb + m2_one_mb)
    one_mb_median = stats.median(m1_one_mb + m2_one_mb)

    axs[1, 0].axvline(one_mb_mean, color='k', linestyle='-', linewidth=1, label="Avg.: " + str(round(one_mb_mean, 4)))
    axs[1, 0].axvline(one_mb_median, color='k', linestyle='--', linewidth=1, label="Med.: " + str(round(one_mb_median, 4)))

    axs[1, 0].set_title('1 MB')
    axs[1, 0].legend(loc="upper left")
    axs[1, 0].xaxis.set_tick_params(labelbottom=True)
    # endregion

    # region 10 MB
    axs[1, 1].hist([m1_ten_mb, m2_ten_mb], density=False, bins=25, rwidth=0.8, label=["L1", "L2"])

    ten_mb_mean = stats.mean(m1_ten_mb + m2_ten_mb)
    ten_mb_median = stats.median(m1_ten_mb + m2_ten_mb)

    axs[1, 1].axvline(ten_mb_mean, color='k', linestyle='-', linewidth=1, label="Avg.: " + str(round(ten_mb_mean, 4)))
    axs[1, 1].axvline(ten_mb_median, color='k', linestyle='--', linewidth=1, label="Med.: " + str(round(ten_mb_median, 4)))

    axs[1, 1].set_title('10 MB')
    axs[1, 1].legend(loc="upper right")
    axs[1, 1].xaxis.set_tick_params(labelbottom=True)
    axs[1, 1].yaxis.set_tick_params(labelbottom=True)
    # endregion

    print("")


def get_data(file_path):
    ten_kb = []
    hundred_kb = []
    one_mb = []
    ten_mb = []

    df = pd.read_csv(file_path, sep=",", header=None)

    for number in df.values[1:]:
        ten_kb.append(number[4])
        hundred_kb.append(number[3])
        one_mb.append(number[2])
        ten_mb.append(number[1])
    
    ten_kb = remove_outliers(ten_kb)
    hundred_kb = remove_outliers(hundred_kb)
    one_mb = remove_outliers(one_mb)
    ten_mb = remove_outliers(ten_mb)
    
    return ten_kb, hundred_kb, one_mb, ten_mb


def remove_outliers(data):
    for i in range(5): # max and min 5%
        data.remove(max(data))
        data.remove(min(data))

    return data


if __name__ == "__main__":
    main()
