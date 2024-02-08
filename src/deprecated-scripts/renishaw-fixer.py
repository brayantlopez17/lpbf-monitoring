import os

import pandas as pd
import numpy as np
from tqdm import tqdm


def create_new_df(filepath:str, scale:float, offset:int, directory:str):

    name = filepath.split('/')[-1]
    df = renishaw_check_df_first_on(filepath, offset)
    df['x'] = df['x'].apply(lambda x: x/scale)
    df['y'] = df['y'].apply(lambda x: x/scale)
    df['z'] = df['z'].apply(lambda x: x/scale)
    df.to_csv(f"{directory}/scaled_{name}", index=False)


def renishaw_check_df_first_on(filepath, offset):
    df = apply_offset_df(filepath, offset)
    msk_lst = df.index[df['Laser Status'] == 1].tolist()
    i, j = msk_lst[0], msk_lst[-1]
    return df[i:j]


def apply_offset_df(filepath:str, offset:int):
    df = pd.read_csv(filepath)
    t = df['t'].map(lambda x: x/2)
    x = np.roll(np.array(df["x'"]), offset)
    y = np.roll(np.array(df["y'"]), offset)
    z = np.roll(np.array(df["z'"]), offset)
    p = np.array(df["L_p"])
    laser_status = np.array(df["L_s"])
    Mvw = np.array(df["Mvw"])
    PVw = np.array(df["PVw"])
    LVw = np.array(df["LVw"])
    f8 = np.array(df["Fill8"])
    f9 = np.array(df["Fill9"])


    df2 = pd.DataFrame(
        {'t': t, "x": x, "y": y, "z": z, "Power": p, "Laser Status": laser_status, "Mvw": Mvw, "PVw": PVw, "LVw": LVw, "Fill8": f8, "Fill9": f9})

    return df2


def renishaw_fix_time(filepath):
    df = pd.read_csv(filepath)
    df['t'] = df['t'].map(lambda x: x*2)
    df.to_csv(filepath, index=False)


if __name__ == "__main__":
    # filepath = "C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/UTEP45-scaled/scaled_id-001_lsr1.csv"
    new_directory = "C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/UTEP45-scaled"
    # old_directory = "C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/converted"

    scale = 200.008
    offset = 42

    for file in tqdm(os.listdir(new_directory), desc="Creating new files", ncols=100):
        filepath = f"{new_directory}/{file}"
        renishaw_fix_time(filepath)
