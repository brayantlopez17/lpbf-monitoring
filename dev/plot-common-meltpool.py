import pandas as pd
import pyvista as pv
import numpy as np


def pv_plot_aconity(filepath, laser_status=True, show=True):
    df = pd.read_csv(filepath)
    x = df['x']
    y = df['y']
    laser = np.array(df['state0'])

    if laser_status:
        points = np.c_[x, y, np.zeros(len(df))]
        point_cloud = pv.PolyData(points)
        point_cloud['laser status'] = laser
        if show:
            point_cloud.plot(render_points_as_spheres=True)
        else:
            return point_cloud
    else:
        grid = pv.StructuredGrid()
        grid.dimensions = [len(x), 1, 1]
        grid.points = pv.pyvista_ndarray(np.c_[x, y, np.zeros(len(x))])
        if show:
            grid.plot(show_edges=True)
        else:
            return grid


def pv_plot_renishaw(filepath, laser_status= True, show=True, only_scanning=True):
    if only_scanning:
        df = renishaw_check_df_first_on(filepath)
    else:
        df = pd.read_csv(filepath)

    x = df["x"]
    y = df["y"]
    laser = df['L_s']

    if laser_status:
        points = np.c_[x, y, np.zeros(len(df))]
        point_cloud = pv.PolyData(points)
        point_cloud['laser status'] = laser
        if show:
            point_cloud.plot(render_points_as_spheres=False)
        else:
            return point_cloud

    else:
        grid = pv.StructuredGrid()
        grid.dimensions = [len(x), 1, 1]
        grid.points = pv.pyvista_ndarray(np.c_[x, y, np.zeros(len(x))])
        if show:
            grid.plot(show_edges=True)
        else:
            return grid


def plot_renishaw_commanded(filepath, laser_status, show, offset):
    df = ren_df_offset(filepath, offset)

    x = df["x'"]
    y = df["y'"]
    laser = df['Laser Status']

    if laser_status:
        points = np.c_[x, y, np.zeros(len(df))]
        point_cloud = pv.PolyData(points)
        point_cloud['laser status'] = laser
        if show:
            point_cloud.plot(render_points_as_spheres=True)
        else:
            return point_cloud

    else:
        grid = pv.StructuredGrid()
        grid.dimensions = [len(x), 1, 1]
        grid.points = pv.pyvista_ndarray(np.c_[x, y, np.zeros(len(x))])
        if show:
            grid.plot(show_edges=True)
        else:
            return grid


def pv_plot_power_renishaw(filepath):

    df = pd.read_csv(filepath)
    filter_on = df['L_s'] == 1
    filer_power = df['L_p'] != 0
    df_on = df[filter_on & filer_power]

    laser_power = df_on['L_p']
    x = df_on["x'"]
    y = df_on["y'"]

    points_np = np.c_[x, y, np.zeros(len(df_on))]
    points = pv.PolyData(points_np)
    points['laser power'] = laser_power

    points.plot(render_points_as_spheres=True)


def pv_plot_eos(filepath, laser_status= True, show=True, only_scanning=True):
    if only_scanning:
        df = eos_df_first_on(filepath)
    else:
        df = pd.read_csv(filepath)

    x = df["x"]
    y = df["y"]
    laser = df['laser_drive']

    if laser_status:
        points = np.c_[x, y, np.zeros(len(df))]
        point_cloud = pv.PolyData(points)
        point_cloud['laser status'] = laser
        if show:
            point_cloud.plot(render_points_as_spheres=True)
        else:
            return point_cloud

    else:
        grid = pv.StructuredGrid()
        grid.dimensions = [len(x), 1, 1]
        grid.points = pv.pyvista_ndarray(np.c_[x, y, np.zeros(len(x))])
        if show:
            grid.plot(show_edges=True)
        else:
            return grid


def pv_plot_slm(filepath, laser_status=True, show=True, only_scanning=True):
    if only_scanning:
        df = slm_df_first_on(filepath)
    else:
        df = pd.read_csv(filepath)

    x = df["x"]
    y = df["y"]
    laser = df["laser"]

    if laser_status:
        points = np.c_[x, y, np.zeros(len(df))]
        point_cloud = pv.PolyData(points)
        point_cloud['laser status'] = laser
        if show:
            point_cloud.plot(render_points_as_spheres=True)
        else:
            return point_cloud

    else:
        grid = pv.StructuredGrid()
        grid.dimensions = [len(x), 1, 1]
        grid.points = pv.pyvista_ndarray(np.c_[x, y, np.zeros(len(x))])
        if show:
            grid.plot(show_edges=True)
        else:
            return grid


def renishaw_check_df_first_on(filepath):
    df = pd.read_csv(filepath)
    msk_lst = df.index[df['L_s'] == 1].tolist()
    i, j = msk_lst[0], msk_lst[-1]
    return df[i:j]


def slm_df_first_on(filepath):
    df = pd.read_csv(filepath)
    msk_lst = df.index[df['laser'] == 1].tolist()
    i, j = msk_lst[0], msk_lst[-1]
    return df[i:j]


def eos_df_first_on(filepath):
    df = pd.read_csv(filepath)
    msk_lst = df.index[df['laser_drive'] == 1].tolist()
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



    df2 = pd.DataFrame({'t':t, "x'":x, "y'":y, "z'":z, "Laser Power":p, "Laser Status":laser_status, "MVw":mvw, "PVw": pvw, "LVw":lvw, "Fill8":f8, "Fill9":f9})

    # df2 = pd.DataFrame({'t':t, "x'":x, "y'":y, "z'":z, "Laser Power":p, "Laser Status":laser_status})
    df2.to_csv("test_ren1.csv")
    return df2







if __name__ == "__main__":
    aconity_file = "C:/Users/braya/HT_Test/MonitoringData/UTEP51 PCD/processed/00_05.csv"
    eos_file = "C:/Users/braya/HT_Test/MonitoringData/UTEP_40/processed/id_089_laser_1.csv"
    renishaw_file = "C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/dat files/processed/id-001_lsr1.csv"
    slm_file = "C:/Users/braya/HT_Test/MonitoringData/UTEP49_F/UTEP49_F/MPM/processed/id_00106_l1.csv"
    renishaw_file2 = "C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/converted/id-001_lsr1.csv"



    # aconity_plt = pv_plot_aconity(filepath=aconity_file, laser_status=True, show=False)
    #eos_plt = pv_plot_eos(filepath=eos_file, laser_status=True, show=True, only_scanning=True)
    #ren_plt = pv_plot_renishaw(filepath=renishaw_file, laser_status=True, show=True, only_scanning=True)

    slm_plt = pv_plot_slm(filepath=slm_file, laser_status=True, show=True, only_scanning=False)

    #plot_renishaw_commanded(filepath=renishaw_file2, laser_status=True, show=True, offset=42)
    #pv_plot_power_renishaw(renishaw_file)
    #
    # plotter = pv.Plotter(shape=(2,2))
    #
    # plotter.subplot(0,0)
    # plotter.add_text("Aconity", font_size=18)
    # plotter.add_mesh(aconity_plt)
    #
    # plotter.subplot(1,0)
    # plotter.add_text("Renishaw", font_size=18)
    # plotter.add_mesh(ren_plt)
    #
    # plotter.subplot(0,1)
    # plotter.add_text("EOS", font_size=18)
    # plotter.add_mesh(eos_plt)
    #
    # plotter.subplot(1,1)
    # plotter.add_text("SLM", font_size=18)
    # plotter.add_mesh(slm_plt)
    # plotter.show()