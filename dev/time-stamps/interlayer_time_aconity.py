import os

import pandas as pd


def get_time_stamps(filepath:str):
    start = 0
    end = 0
    with open(filepath, 'r') as file:
        for line in file:
            if "# sample.start" in line:
                i = line.rfind("=")
                start = int(line[i+2:])
            if "# sample.end" in line:
                j = line.rfind("=")
                end = int(line[j+2:])
            if start != 0 and end != 0:
                return start, end


def aconity_layer_num(file:str):
    k = file.find(".")
    val = file[:k]
    val = val.replace("_", ".")
    val = float(val)

    return round(val/0.05)



if __name__ == "__main__":

    # file1 = "40_10.pcd"
    # file2 = "40_15.pcd"
    #
    # print(aconity_layer_num(file1), aconity_layer_num(file2))
    layer = []
    start_ls = []
    end_ls = []

    directory = 'C:/Users/braya/HT_Test/MonitoringData/UTEP51 PCD/UTEP51 PCD'
    for file in os.listdir(directory):
        i = aconity_layer_num(file)
        filepath = os.path.join(directory, file)
        start, end = get_time_stamps(filepath)
        layer.append(i)
        start_ls.append(start)
        end_ls.append(end)
        print(f"{file} -> {i}")


    table = zip(layer, start_ls, end_ls)
    with open("time_stamps_aconity.csv", 'w') as file:
        file.write("layer,start,end\n")
        for row in table:
            file.write(f"{row[0]},{row[1]},{row[2]}\n")

