"""
This class will contain the methods to visualize layers from the common monitoring file
using different libraries depending on the purpose of the visual.
matplotlib -> get precise values of point coordinates
pyvista -> quick render and coloring of laser on and off
plotlyexpress -> nice rendering
"""

# Libs
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import pyvista as pv

__author__ = 'Brayant Lopez'
__copyright__ = 'Copyright 2023, Tailored Alloys'
__license__ = 'MIT'
__version__ = '0.1.0'

# Global Variables
LAYER = 1
LASER_ON = True
LASER_OFF = False
PLOTTING_LIB = 'pv'                             #pv: pyvista, px:plotly, plt:matplotlib

dx = -140-0.14610
dy = -135-0.08365


class CommonMonitoringPlotter:
    """
    Class that takes a file from the common monitoring file format and is
    used to plot the layer geometry. Laser on and off.
    """
    def __init__(self, filepath:str):
        self.filepath = filepath
        self._df = pd.read_csv(filepath)

        self.df_plot = self._filter_df()
        self._translate_layer(0, 0)
        self.rotate_theta(90)


    def _filter_df(self, laser_on=LASER_ON, laser_off=LASER_OFF):
        if laser_on and laser_off:
            return self._df
        elif laser_on and not laser_off:
            return self._df[self._df['laser_status'] == 1]
        elif laser_off and not laser_on:
            return self._df[self._df['laser_status'] == 0]

    def _translate_layer(self, x, y):
        """
        Translate the layer by x and y
        """
        self._df['x'] = self._df['x'] + x
        self._df['y'] = self._df['y'] + y

    def rotate_theta(self, theta):
        """
        Rotate the layer by theta degrees
        """
        theta = np.radians(theta)
        x_axis, y_axis = self._df['x'], self._df['y']
        x_axis_rotated = x_axis*np.cos(theta) - y_axis*np.sin(theta)
        y_axis_rotated = x_axis*np.sin(theta) + y_axis*np.cos(theta)
        self._df['x'], self._df['y'] = x_axis_rotated, y_axis_rotated

    def plot_layer_pv(self):
        x_axis, y_axis, laser = self.df_plot['x'], self.df_plot['y'], np.array(self.df_plot['laser_status'])

        points = np.c_[x_axis, y_axis, np.zeros(len(self.df_plot))]
        point_cloud = pv.PolyData(points)
        point_cloud['laser status'] = laser
        point_cloud.plot(render_points_as_spheres=True)

    def plot_layer_plotly(self, laser_on=LASER_ON, laser_off=LASER_OFF):
        df = self._filter_df(laser_on=laser_on, laser_off=laser_off)
        fig = px.scatter(df, x='x', y='y')
        fig.show()

if __name__ == "__main__":
    filepath = r"C:\Users\braya\HT_Test\MonitoringData\UTEP49_F\UTEP49_F\MPM\data\scaled\1-99\slm-id_00002_l1_scaled.csv"
    #filepath = "C:/Users/braya/HT_Test/MonitoringData/UTEP_40/processed/UTEP40-scaled/scaled_id_170_laser_1.csv"
    plotter = CommonMonitoringPlotter(filepath)

    # plotter.plot_layer_plotly(laser_on=True, laser_off=False)
    plotter.plot_layer_pv()



# def plot_layer_pv(layer_num=LAYER, laser_on=LASER_ON, laser_off=LASER_OFF):

