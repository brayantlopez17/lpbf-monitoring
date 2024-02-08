import os

import h5py
import csv


def h5(filepath, output_file):

    """
    Data exploration

    Given the h5 file, show 3 matplotlib plots in a row:
        xy coordinates
        laser signal
        power signal

    All 3 above plots start at start int, and end at start + num_points
    """

    f = h5py.File(filepath, 'r')
    lasers = f['LASERS']
    one = lasers['1']

    laser_drive = map(lambda x:x//3, one['Laser Drive'][22:])
    laser_power = one['Laser Power'][22:]
    on_high = one['On-Axis HIGH'][22:]
    on_low = one['On-Axis LOW'][22:]
    on_ted = one['On-Axis TED'][22:]
    sync_puls = one['Sync Pulse']
    x = one['X-Position'][:-22]
    y = one['Y-Position'][:-22]
    t = [i*10 for i in range(len(x))]

    lst = zip(t,x,y,laser_power, laser_drive, on_high, on_low, on_ted, sync_puls)

    with open(output_file, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['t','x', 'y', 'laser_power', 'laser_drive', 'on_high', 'on_low', 'on_ted', 'sync_puls'])
        wr.writerows(lst)


def output_file(filepath:str):
    i = filepath.rfind("_")
    substring1 = filepath[:i]
    j = substring1.rfind("_")
    return f"id_{substring1[j+1:]}_laser_1.csv"





if __name__ == "__main__":
    dir = "C:/Users/braya/HT_Test/MonitoringData/UTEP_40"
    for file in os.listdir(dir):
        file_name = output_file(file)
        in_file = f"{dir}/{file}"
        out_filepath = f"C:/Users/braya/HT_Test/MonitoringData/UTEP_40/processed/{file_name}"
        h5(in_file, out_filepath)
        print(f"finished {file_name}")
