# Created By: Daniyal Khan
# Goal: To process PCD file and convert it to CSV file format
import pandas as pd, numpy as np, os
# from .PCD_correction import *


def PCDProcess(path):
    """
    The function takes in a path to a PCD file, preprocesses the data, converts units, calculates
    distance and velocity, and returns a pandas dataframe.

    :param path: The file path of the PCD file to be processed
    :param CONFIG: A dictionary containing various configuration parameters for the PCD file, such as
    time delay, field size, scaling, and offset values for X and Y coordinates
    :return: The function `PCDProcess` returns a pandas DataFrame containing preprocessed data from a
    PCD file.
    """

    # PCD Correction
    # recorrect_path = os.path.join(os.path.dirname(path), 'temp')
    # output = os.path.join(recorrect_path, os.path.basename(path))
    # os.mkdir(recorrect_path)
    # print(recorrect_path)
    # recorrect_pcd_file(path, CONFIG['field_correction_file'], output)
    # path = output

    # Processing Corrected PCD
    FILE_NAME = path
    layer_thickness = path[path.rfind("/")+1:path.rfind(".")].replace(".","_")
     # Reading the PCD file as CSV
    columns = [
        "t",
        "x",
        "y",
        "z",
        "sensor0",
        "sensor1",
        "sensor2",
        "sensor3",
        "state0",
        "state1",
    ]

    filepath = f"C:/users/braya/HT_Test/MonitoringData/UTEP51 PCD/processed/{layer_thickness}.csv"
    with open(path, 'r+') as fp:
        # read an store all lines into list
        lines = fp.readlines()
        # move file pointer to the beginning of a file
        fp.seek(0)
        # truncate the file
        fp.truncate()

        # start writing lines except the first line
        # lines[1:] from line 2 to last line
        fp.writelines(lines[1:-1])

    reader = pd.read_csv(
        FILE_NAME,
        delimiter=" ",
        skiprows=23,
        header=3,
        dtype={
            0: int,
            1: float,
            2: float,
            3: float,
            4: int,
            5: int,
            6: int,
            7: int,
            8: int,
            9: int,
        },
    )
    reader.columns = columns

    # The code is shifting the values in the columns 'sensor0', 'sensor1', 'sensor2', 'sensor3',
    # 'state0', and 'state1' by 8 positions to the right using the numpy function `np.roll()`. This
    # operation is done to align the data and compensate for the difference between sensor start time
    # and laser movement start time.
    reader['sensor0'] = np.roll(reader['sensor0'], 8)
    reader['sensor1'] = np.roll(reader['sensor1'], 8)
    reader['sensor2'] = np.roll(reader['sensor2'], 8)
    reader['sensor3'] = np.roll(reader['sensor3'], 8)
    reader['state0'] = np.roll(reader['state0'], 8)
    reader['state1'] = np.roll(reader['state1'], 8)
    # Converting the time unit
    reader["t"] = reader["t"] * 10 ** -6



    reader.to_csv(filepath, index=False)
    print(f"{layer_thickness} finished")

    return reader

if __name__ == "__main__":
    directory = 'C:/Users/braya/HT_Test/MonitoringData/UTEP51 PCD/UTEP51 PCD'
    for files in os.listdir(directory):
        PCDProcess(f"{directory}/{files}")