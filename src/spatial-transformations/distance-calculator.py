import os

import numpy as np
from tqdm import tqdm
import pandas as pd

def get_aconity_layer(file):
    k = file.find(".")
    val = file[:k]
    val = val.replace("_", ".")
    val = float(val)

    return round(val / 0.05)


def travel_distance_acon(filename, scale:float):


    ren_csv = pd.read_csv(filename)
    ren_csv['Length'] = np.sqrt(ren_csv["x"].diff()**2 + ren_csv["y"].diff()**2)

    filter_on = ren_csv['state0'] == 1
    on_sum = ren_csv[filter_on]
    travel_d_on = on_sum['Length'].sum()/ scale
    time_on = len(on_sum)*10/1000000

    filter_off = ren_csv['state0'] == 0
    off_sum = ren_csv[filter_off]
    travel_d_off = off_sum['Length'].sum()/ scale
    time_off = len(off_sum)*10/1000000
    return (travel_d_off, time_off, travel_d_on, time_on)


def renishaw_check_df_first_on(filepath):
    df = pd.read_csv(filepath)
    df['t'] = df['t'].apply(lambda x:x/2)
    msk_lst = df.index[df['Laser Status'] == 1].tolist()
    i, j = msk_lst[0], msk_lst[-1]
    return df[i:j]


def travel_distance_renishaw(filename, scale:float):
    ren_csv = renishaw_check_df_first_on(filename)

    ren_csv['length'] = np.sqrt(ren_csv["x"].diff()**2 + ren_csv["y"].diff()**2)

    filter_on = ren_csv['laser_status'] == 1
    on_sum = ren_csv[filter_on]
    travel_d_on = (on_sum['length'].sum())/scale
    time_on = len(on_sum)*10/1000000

    filter_off = ren_csv['laser_status'] == 0
    off_sum = ren_csv[filter_off]
    travel_d_off = (off_sum['length'].sum())/scale
    time_off = len(off_sum)*10/1000000

    return (travel_d_off, time_off, travel_d_on, time_on)


def travel_distance_eos(filename, scale:float):

    ren_csv = pd.read_csv(filename)
    ren_csv['length'] = np.sqrt(ren_csv["x"].diff()**2 + ren_csv["y"].diff()**2)

    filter_on = ren_csv['Laser Status'] == 1
    on_sum = ren_csv[filter_on]
    travel_d_on = on_sum['length'].sum()/scale
    time_on = len(on_sum)*10/1000000

    filter_off = ren_csv['Laser Status'] == 0
    off_sum = ren_csv[filter_off]
    travel_d_off = off_sum['length'].sum()/scale
    time_off = len(off_sum)*10/1000000
    return (travel_d_off, time_off, travel_d_on, time_on)


def travel_distance_slm(filename, scale:float):

    ren_csv = fix_slm_df(filename)
    ren_csv['Length'] = np.sqrt(ren_csv["x"].diff()**2 + ren_csv["y"].diff()**2)

    filter_on = ren_csv['laser'] == 1
    on_sum = ren_csv[filter_on]
    travel_d_on = on_sum['Length'].sum()/scale
    time_on = len(on_sum)*10/1000000

    filter_off = ren_csv['laser'] == 0
    off_sum = ren_csv[filter_off]
    travel_d_off = off_sum['Length'].sum()/scale
    time_off = len(off_sum)*10/1000000
    return (travel_d_off, time_off, travel_d_on, time_on)


def fix_slm_df(filename):
    """
    drops the first entry of the slm csv file
    """
    df = pd.read_csv(filename)
    return df.iloc[1:]


def fix_eos_df(filename):
    df = pd.read_csv(filename)
    i, j = 0, 0
    x, y = [], []

    x0 = list(df["x"][::2])
    x1 = list(df["x"][1::2])

    while i < len(x0):
        x.append(x1[i])
        x.append(x0[i])
        i += 1

    y0 = list(df["y"][::2])
    y1 = list(df["y"][1::2])
    while j != len(y0):
        y.append(y1[j])
        y.append(y1[j])
        j += 1

    df["x"] = x
    df["y"] = y
    return df


if __name__ == "__main__":

    #eos_dir = "C:/Users/braya/HT_Test/MonitoringData/UTEP_40/processed/UTEP40-scaled"
    #renishaw_dir = "C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/UTEP45-scaled/"
    slm_dir = "C:/Users/braya/HT_Test/MonitoringData/UTEP49_F/UTEP49_F/MPM/processed/"
    #aconity_dir = "C:/Users/braya/HT_Test/MonitoringData/UTEP51 PCD/processed/"

    layer, time_on, time_off, time_expo, distance_on, distance_off, total_distance = [], [], [], [], [], [], []

    i = 1
    for file in tqdm(os.listdir(slm_dir), desc="Processing Files", ncols=100, colour="green"):
        # i = get_aconity_layer(file)
        slm_filepath = f"{slm_dir}/{file}"

        # off_dist, off_time, on_dist, on_time = travel_distance_renishaw(renishaw_filepath, 1)
        # off_dist, off_time, on_dist, on_time = travel_distance_eos(eos_filepath, scale=1)
        # off_dist, off_time, on_dist, on_time = travel_distance_acon(aconity_filepath)
        off_dist, off_time, on_dist, on_time = travel_distance_slm(slm_filepath, scale=234.1942)

        layer.append(i)
        i += 1
        time_on.append(on_time), time_off.append(off_time), time_expo.append(on_time+off_time)
        distance_on.append(on_dist/1000), distance_off.append(off_dist/1000), total_distance.append((on_dist+off_dist)/1000)

    table = zip(layer, time_on, time_off, time_expo, distance_on, distance_off, total_distance)

    with open("../data/slm_summary_final.csv", 'w') as f:
        f.write("Layer, Time On, Time Off, Time Expo, Distance On, Distance Off, Total Distance\n")
        for row in table:
            f.write(f"{row[0]}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}, {row[6]}\n")



    # print("time on: ", on_time)
    # print("time off: ", off_time)
    # print("time expo: ", (on_time+off_time))
    # print("distance on: ", on_dist/1000)
    # print("distance off: ", off_dist/1000)
    # print("total distance: ", (on_dist+off_dist)/1000)
