import numpy as np
import pandas as pd
import pyvista as pv
import plotly.express as px

LASER_ON = True
LASER_OFF = True


def open_df(filepath:str, laser_on=LASER_ON, laser_off=LASER_OFF):
    df = pd.read_csv(filepath)
    if laser_on and laser_off:
        return df
    elif laser_on and not laser_off:
        return df[df['laser_status'] == 1]
    elif laser_off and not laser_on:
        return df[df['laser_status'] == 0]


def plot_layer_pv(filepath:str):
    df_plot = open_df(filepath)
    x_axis, y_axis, laser = df_plot['x'], df_plot['y'], np.array(df_plot['laser_status'])

    points = np.c_[x_axis, y_axis, np.zeros(len(df_plot))]
    point_cloud = pv.PolyData(points)
    point_cloud['laser status'] = laser
    point_cloud.plot(render_points_as_spheres=True)


def plot_layer_plotly(filepath:str):
    df_plot = open_df(filepath)
    fig = px.scatter(df_plot, x='x', y='y',
                     color='laser_status',
                     color_continuous_scale='viridis')
    fig.show()