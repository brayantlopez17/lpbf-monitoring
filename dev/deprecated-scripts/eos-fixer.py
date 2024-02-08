import os

import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


def eos_df_first_on(filepath, offset):
    df = pd.read_csv(filepath)
    t = df['t']
    x = np.roll(np.array(df["x"]), offset)
    y = np.roll(np.array(df["y"]), offset)
    p = np.array(df["laser_power"])
    laser_status = np.array(df["laser_drive"])
    on_high = np.array(df["on_high"])
    on_low = np.array(df["on_low"])
    on_ted = np.array(df["on_ted"])

    df2 = pd.DataFrame(
        {'t': t, "x": x, "y": y,"Power": p, "Laser Status": laser_status, "on_high": on_high, "on_low": on_low,
         "on_ted": on_ted})

    return df2


def fix_eos_df(filename, offset):
    df = eos_df_first_on(filename, offset)
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


def trim_eos_values(filepath, offset):
    df = fix_eos_df(filepath, offset)
    msk_lst = df.index[df['Laser Status'] == 1].tolist()
    i, j = msk_lst[0], msk_lst[-1]
    return df[i:j]


def create_new_df(filepath:str, scale:float, offset:int, directory:str):
    name = filepath.split('/')[-1]
    df = trim_eos_values(filepath, offset)
    df['x'] = df['x']/scale
    df['y'] = df['y']/scale
    df.to_csv(f"{directory}/scaled_{name}", index=False)


if __name__ == "__main__":

    # file = "C:/Users/braya/HT_Test/MonitoringData/UTEP_40/processed/id_774_laser_1.csv"
    # filepath = "C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/converted/id-774_lsr1.csv"
    new_directory = "C:/Users/braya/HT_Test/MonitoringData/UTEP_40/processed/scaled"
    old_directory = 'C:/Users/braya/HT_Test/MonitoringData/UTEP_40/processed'

    scale = 0.06202
    offset = 0

    for file in tqdm(os.listdir(old_directory), desc="Creating new files", ncols=100):
        old_filepath = f"{old_directory}/{file}"
        new_filepath = f"{new_directory}/scaled_{file}"
        if file.endswith("csv"):
            create_new_df(old_filepath, scale, offset, new_directory)
