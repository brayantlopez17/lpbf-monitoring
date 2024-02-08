import csv
from tqdm import tqdm
import pandas as pd
import os

def calculate_z_from_filepath(file):
    """
    Calculates z value from filepath.
    """
    i = file.rfind("-")
    j = file.rfind("_")
    return round(int(file[i+1:j])*.05, 4)

if __name__ == "__main__":
    directory = "C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/UTEP45-scaled"
    # merged_df = pd.DataFrame(columns=["x", "y", "z"])
    with open("merged_contours.csv", "w") as file:
        file.write("x,y,z\n")
    with open("merged_contours.csv", "a", newline='') as append_file:
        for file in tqdm(os.listdir(directory), desc="Merging Contours", ncols=100):
            df = pd.read_csv(os.path.join(directory, file))
            df = df[df['Laser Status'] == 1]
            df = df[(df["Power"] == 2864) | (df["Power"] == 0) | (df["Power"] == 1665)]
            z_val = calculate_z_from_filepath(file=file)
            z = [z_val for x in range(len(df.index))]
            x = list(df['x'])
            y = list(df['y'])
            table = zip(x, y, z)
            writer = csv.writer(append_file)
            writer.writerows(table)