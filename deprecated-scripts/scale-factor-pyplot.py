import plotly.express as px
import pandas as pd
import numpy as np


def visualize_eos(filepath:str):
    df = pd.read_csv(filepath)
    # df = df[df['laser_drive'] == 1]
    x = df['x']
    y = df['y']
    l = df['Laser Status']

    fig = px.scatter(x=x, y=y, color=l, height=600, width=600)
    fig.update_traces(marker=dict(size=2))
    fig.update_layout(title="EOS")

    fig.show()


def visualize_renishaw_commanded(filepath:str):
    # df = renishaw_check_df_first_on(filepath)
    df = pd.read_csv(filepath)
    # df = df[df['L_s'] == 1]
    x = df["x"]
    y = df["y"]
    l = df['Laser Status']

    fig = px.scatter(x=x, y=y, color=l, height=600, width=600)
    fig.update_traces(marker=dict(size=2))
    fig.update_layout(title="Renishaw")
    fig.show()


def visualize_slm(filepath:str):
    df = pd.read_csv(filepath)
    # df = df[df['laser'] == 1]
    # df = df[(df['t'] > 2073510) & (df['t'] < 3100990)]
    x = df["x"]
    y = df["y"]
    l = df['Laser Status']

    fig = px.scatter(x=x, y=y, color=l, height=600, width=600)
    fig.update_traces(marker=dict(size=2))
    fig.update_layout(title="SLM")
    fig.show()


def visualize_aconity(filepath:str):
    df = pd.read_csv(filepath)
    # df = df[df['state0'] == 0]
    # df = df[df['t'] > 2073510 & df['t'] < 3100990]
    x = df["x"]
    y = df["y"]
    t = df["state0"]

    fig = px.scatter(x=x, y=y, height=600, width=600, color=t)
    fig.update_traces(marker=dict(size=2))
    fig.update_layout(title="Aconity")
    fig.show()


def renishaw_check_df_first_on(filepath):
    df = ren_df_offset(filepath, 42)
    msk_lst = df.index[df['L_s'] == 1].tolist()
    i, j = msk_lst[0], msk_lst[-1]
    return df[i:j]


def ren_df_offset(filepath, offset):
    df = pd.read_csv(filepath)

    t = np.roll(np.array(df['t'].map(lambda x: x/2)), offset)
    x = np.roll(np.array(df["x'"]), offset)
    y = np.roll(np.array(df["y'"]), offset)
    z = np.roll(np.array(df["z'"]), offset)
    p = np.array(df["L_p"])
    laser_status = np.array(df["L_s"])
    mvw = np.array(df["Mvw"])
    pvw = np.array(df["PVw"])
    lvw = np.array(df["LVw"])
    f8 = np.array(df["Fill8"])
    f9 = np.array(df["Fill9"])



    df2 = pd.DataFrame({'t':t, "x'":x, "y'":y, "z'":z, "L_p":p, "L_s":laser_status, "MVw":mvw, "PVw": pvw, "LVw":lvw, "Fill8":f8, "Fill9":f9})

    # df2 = pd.DataFrame({'t':t, "x'":x, "y'":y, "z'":z, "Laser Power":p, "Laser Status":laser_status})
    df2.to_csv("test_ren1.csv")
    return df2

if __name__ == "__main__":
    layer_num = 774
    filepath_renishaw = f"C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/UTEP45-scaled/scaled_id-{layer_num}_lsr1.csv"
    filepath_eos = "C:/Users/braya/HT_Test/MonitoringData/UTEP_40/processed/scaled/scaled_id_774_laser_1.csv"
    filepath_slm = "C:/Users/braya/HT_Test/MonitoringData/UTEP_40/processed/UTEP40-scaled/scaled_id_774_laser_1.csv"
    filepath_aconity = "C:/Users/braya/HT_Test/MonitoringData/UTEP51 PCD/processed/16_00.csv"

    #visualize_eos(filepath_eos)
    visualize_renishaw_commanded(filepath_renishaw)
    #visualize_slm(filepath_slm)
    #visualize_aconity(filepath_aconity)