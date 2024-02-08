import os

import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


def slm_first_filter(filepath, offset):

    df = pd.read_csv(filepath)
    if offset > 0:
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
    else:
        df.rename(columns={'x': 'x', 'y': 'y', 'laser': 'Laser Status', 'power': '', 'on_high': 'on_high', 'on_low': 'on_low', 'on_ted': 'on_ted'}, inplace=True)


def trim_slm_values(filepath, offset):
    df = slm_first_filter(filepath, offset)
    msk_lst = df.index[df['Laser Status'] == 1].tolist()
    i, j = msk_lst[0], msk_lst[-1]
    return df[i:j]


def create_new_df(filepath:str, scale:float, offset:int, directory:str):
    name = filepath.split('/')[-1]
    df = trim_slm_values(filepath, offset)
    df['x'] = df['x']/scale
    df['y'] = df['y']/scale
    df.to_csv(f"{directory}/scaled_{name}", index=False)


if __name__ == "__main__":

    # file = "C:/Users/braya/HT_Test/MonitoringData/UTEP_40/processed/id_774_laser_1.csv"
    # filepath = "C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/converted/id-774_lsr1.csv"
    new_directory = "C:/Users/braya/HT_Test/MonitoringData/UTEP_40/processed/scaled"
    old_directory = 'C:/Users/braya/HT_Test/MonitoringData/UTEP_40/processed'

    scale = 234.1942
    offset = 0

    for file in tqdm(os.listdir(old_directory), desc="Creating new files", ncols=100):
        old_filepath = f"{old_directory}/{file}"
        new_filepath = f"{new_directory}/scaled_{file}"
        if file.endswith("csv"):
            create_new_df(old_filepath, scale, offset, new_directory)
