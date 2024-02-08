import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def time_summary_renishaw(filepath:str):
    df = pd.read_csv(filepath)
    filter_on = df['L_s'] == 1
    filter_off = df['L_s'] == 0

    df_on = df[filter_on]
    df_off = df[filter_off]

    time_on = len(df_on['t'])*10/(1_000_000)
    time_off = len(df_off['t'])*10/(1_000_000)
    return time_on, time_off


def time_summary_aconity(filepath:str):
    df = pd.read_csv(filepath)
    filter_on = df['state0'] == 1
    filter_off = df['state0'] == 0

    df_on = df[filter_on]
    df_off = df[filter_off]

    time_on = len(df_on['t'])*.00001
    time_off = len(df_off['t'])*.00001
    return time_on, time_off

def aconity_layer_num(file:str):
    k = file.find(".")
    val = file[:k]
    val = val.replace("_", ".")
    val = float(val)

    return round(val/0.05)


def time_summary_sigma_labs(filepath:str):
    df = pd.read_csv(filepath)
    filter_on = df['laser_drive'] == 1
    filter_off = df['laser_drive'] == 0

    df_on = df[filter_on]
    df_off = df[filter_off]

    time_on = len(df_on['t'])*.00001
    time_off = len(df_off['t'])*.00001
    return time_on, time_off


def time_summary_slm(filepath:str):
    df = pd.read_csv(filepath)
    filter_on = df['laser'] == 1
    filter_off = df['laser'] == 0

    df_on = df[filter_on]
    df_off = df[filter_off]

    time_on = len(df_on['t'])*.00001
    time_off = len(df_off['t'])*.00001
    return time_on, time_off

if __name__ == "__main__":


    dir = "C:/Users/braya/HT_Test/MonitoringData/UTEP51 PCD/processed"

    with open("summary_aconity_fixed.csv", "w") as output_file:
        output_file.write("id,on,off\n")
        for file in os.listdir(dir):
            i = aconity_layer_num(file)
            i_str = str(i)
            output_file.write(f"{i_str},")
            fs = f"{dir}/{file}"
            on, off = time_summary_aconity(fs)
            output_file.write(f"{on},{off}\n")
            print(f"appended layer {i} <- {file}")






