import pandas as pd
import numpy as np
import plotly.express as px


class Layer:

    def __init__(self, filepath: str):
        self.df = pd.read_csv(filepath)
        self.df['length'] = self.df['length'] = np.sqrt(self.df["x"].diff() ** 2 + self.df["y"].diff() ** 2)

    def get_number_events_on(self):
        """
        Number of events on indicates when the laser status changed from
        off --> on
        """
        pass

    def get_number_events_off(self):
        """
        Number of events on indicates when the laser status changed from
        on --> off
        """
        pass

    def get_distance_on(self):
        """
        Indicates the total distance when the laser was ON
        """
        pass

    def get_distance_off(self):
        """
        Indicates the total distance when the laser was off
        """
        pass

    def get_time_on(self):
        """
        Indicates the total time that the laser was on
        """
        pass

    def get_time_off(self):
        """
        Indicates the total time that the laser was off
        """
        pass

    def plot(self, show_off: bool):
        """
        Create a plot of the layer, give the option to show when laser was on/off
        """
        pass
