import csv
from tqdm import tqdm
import pandas as pd
import os
import datetime


def segment_contour_by_power(filepath:str, power:list[int], variance:int=0):
    df = pd.read_csv(filepath)
    df = df[df['laser_status'] == 1]
    df_ls = []
    for power_val in power:
        df_temp = df[(power_val - variance < df['power']) & (df['power'] < power_val + variance)]
        df_temp = df_temp[['x', 'y', 'z']]
        df_ls.append(df_temp)
    return pd.concat(df_ls)


def create_merged_contour_csv(output_name:str, dir_monitoring:str, power:list[int]):
    start_empty_csv(output_name)
    for monitoring_file in tqdm(os.listdir(dir_monitoring), desc="Merging Contours", ncols=100, colour="green"):
        filepath = os.path.join(dir_monitoring, monitoring_file)
        df = segment_contour_by_power(filepath=filepath, power=power, variance=10)
        df.to_csv(output_name, mode='a', index=False, header=False)


def start_empty_csv(name:str):
    open(name, 'w').close()
    file = open(name, "w")
    file.write("x,y,z\n")
    file.close()


def create_pcd(output_file, input_file, scale:float):
    # file = open(output_file, "w")
    df = pd.read_csv(input_file)
    df['x'] = df['x']/scale
    df['y'] = df['y']/scale
    # file.write(f"# This PCD file was generated from the monitoring file contours\n"
    #            f"# Date {datetime.datetime.today()}\n"
    #            f"VERSION .7\n"
    #            f"FIELDS x y z\n"
    #            f"SIZE 4 4 4\n"
    #            f"SIZE 4 4 4\n"
    #            f"COUNT 1 1 1\n"
    #            f"WIDTH {len(df)}\n"
    #            f"HEIGHT 1\n"
    #            f"VIEWPOINT 0 0 0 1 0 0 0\n"
    #            f"POINTS {len(df)}\n"
    #            f"DATA ascii\n")

    df.to_csv(output_file, mode="w", index=False, header=True)





if __name__ == "__main__":

    create_pcd("UTEP49_Merged_Contours_scaled.csv", "UTEP49_Merged_Contours.csv", scale= 234.1942)


