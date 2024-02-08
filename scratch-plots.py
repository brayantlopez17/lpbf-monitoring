import os

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm


def layer_number_string(l:int) -> str:
    i = l/10
    if i < 1:
        return f"00{l}"
    if 1 <= i < 10:
        return f"0{l}"
    if i >= 10:
        return f"{l}"

def calculate_z_from_filepath(filepath:str) -> float:
    i = int(filepath[filepath.rfind("-")+1:filepath.rfind("_")])
    return round(i*.05, 4)


def visualize_renishaw(filepath:str):
    df = pd.read_csv(filepath)
    df = df[df['Laser Status'] == 1]
    # df = df[(df['t'] > 5011920) & (df['t'] < 6926000)]
    x = df["x"]
    y = df["y"]

    plt.scatter(x, y)
    plt.show()


def fix_renishaw_files(filepath):
    df = pd.read_csv(filepath)
    t = df['t']/2
    z_val = calculate_z_from_filepath(filepath)
    z = [z_val for i in range(len(df))]
    x,y,power, laser = df['x'], df['y'], df['Power'], df['Laser Status']
    mvw, pvw, lvw, f8, f9 = df['MVw'], df['PVw'], df['LVw'], df['Fill8'], df['Fill9']
    new_df = {'t': t, 'x': x, 'y': y, 'z': z, 'power': power, 'laser_status': laser, 'mvw': mvw, 'lvw':lvw, 'fill_1':f8, 'fill_2':f9 }
    df2 = pd.DataFrame.from_dict(new_df)
    df2.to_csv(filepath)


def _fix_again(filepath):
    df = pd.read_csv(filepath)
    df.drop('Unnamed: 0', axis=1, inplace=True)
    df.drop('Unnamed: 0.1', axis=1, inplace=True)
    df.to_csv(filepath, index=False)


def translate_fix_time(filepath:str):
    filename = filepath[filepath.rfind("/")+1:]
    df = pd.read_csv(filepath)
    # df['t'] = df['t']*2
    df['x'] = df['x'] - 277.843
    df['y'] = df['y'] - 50.261
    df['z'] = df['z'] - 18.027
    # df.drop('Unnamed: 0', axis=1, inplace=True)
    df.to_csv(f"C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/UTEP45-scaled/output/{filename}")

def layer_thickness_to_num(filepath:str)->int:
    """
    takes the filename from the pcd file, retrieves the layer height and outputs the layer number
    :return: layer num as int
    """
    layer_thickness = filepath[filepath.rfind("/") + 1:filepath.rfind(".")].replace(".", "_")
    layer_num = int(round(float(layer_thickness), 4)/(.05*100))
    return layer_num
def fix_aconity_names_and_columns(filepath):
    filepath = filepath.replace("\\", "/")
    layer_num = layer_thickness_to_num(filepath)
    new_name = f'acon-id_{layer_num}_l1.csv'

    df = pd.read_csv(filepath)
    print(df.head(10))







if __name__ == "__main__":
    l = [1, 170, 320]
    # filepath = r"C:\Users\braya\HT_Test\MonitoringData\UTEP 45\UTEP 45\UTEP45-scaled\scaled_id-002_lsr1.csv"
    # translate_fix_time(filepath)
    # layer = layer_number_string(l)
    dir_path = "C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/monitor_files"

    filepath = r"C:\Users\braya\HT_Test\MonitoringData\UTEP51 PCD\processed\01_20.csv"
    fix_aconity_names_and_columns(filepath)


