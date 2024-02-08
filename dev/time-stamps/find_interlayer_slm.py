import pandas as pd


def clean_df(filepath):
    df = pd.read_csv(filepath)

    df['Exposure (s)'] = df['Exposure Time'].apply(lambda x: float(x[x.rfind(":")+1:]))
    df['Recoating (s)'] = df['Recoating Time'].apply(lambda x: float(x[x.rfind(":")+1:]))

    df.to_csv("interlayer time slm fixed.csv")


def convert_to_sec(ts:str):
    i = ts.rfind(":")
    return float(ts[i:])


if __name__ == "__main__":

    filepath = "C:/Users/braya/Downloads/slm_interlayer.csv"

    clean_df(filepath)


    # filepath = "C:/Users/braya/Downloads/log_fixed_slm.txt"
    #
    # layer = []
    # starting_expo = []
    # finish_expo =[]
    # starting_recoating = []
    #
    # starting_recoating.append(0)
    # i = 1
    #
    # with open(filepath, 'r') as file:
    #     for line in file:
    #         # print(line[:19])
    #
    #         if "Starting exposure" in line:
    #             starting_expo.append(line[:19])
    #             layer.append(i)
    #             i += 1
    #         if "Exposure finished" in line:
    #             finish_expo.append(line[:19])
    #         if "Starting recoating" in line:
    #             starting_recoating.append(line[:19])