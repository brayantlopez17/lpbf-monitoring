import pandas as pd
import numpy as np
import plotly.express as px


class Layer:

    def __init__(self, filepath: str):
        self.df = pd.read_csv(filepath)
        self.df['length'] = self.df['length'] = np.sqrt(
            self.df["x"].diff() ** 2 + self.df["y"].diff() ** 2)

    def get_number_events_on(self):
        """
        Number of events on indicates when the laser status changed from
        off --> on
        """
        # Define the shift column to move down one index
        self.df["shift"] = self.df["laser_status"].shift()

        # Define the on_count (Number of times laser_status went off --> on)
        on_events = 0

        # Iterate through the dataframe using indexes
        for index, rows in self.df.iterrows():

            # Defines the old and new values
            old = self.df["shift"][index]
            new = self.df["laser_status"][index]

            # Compares the values to determine if the laser went off-->on
            if old == 0 and new == 1:
                on_events += 1

        return on_events

    def get_number_events_off(self):
        """
        Number of events on indicates when the laser status changed from
        on --> off
        """
        # Define the shift column to move down one index
        self.df["shift"] = self.df["laser_status"].shift()

        # Define the off_count (Number of times laser_status went on --> off)
        off_events = 0

        # Iterate through the dataframe using indexes
        for index, rows in self.df.iterrows():

            # Defines the old and new values
            old = self.df["shift"][index]
            new = self.df["laser_status"][index]

            # Compares the values to determine if the laser went on-->off
            if old == 1 and new == 0:
                off_events += 1

        return off_events

    def get_distance_on(self):
        """
        Indicates the total distance when the laser was ON
        """
        onDF = self.df[self.df["laser_status"] == 1]
        return onDF.sum()["length"]

    def get_distance_off(self):
        """
        Indicates the total distance when the laser was off
        """
        # Define distance_on
        offDF = self.df[self.df["laser_status"] == 0]
        return offDF.sum()["length"]

    def get_time_on(self):
        """
        Indicates the total time that the laser was on
        """
        on_count = 0

        # Iterate through the data frame
        for index, rows in self.df.iterrows():
            # Determine if the laser is on
            if self.df["laser_status"][index] == 1:
                on_count += 1

        return on_count

    def get_time_off(self):
        """
        Indicates the total time that the laser was off
        """
        off_count = 0

        # Iterate through the data frame
        for index, rows in self.df.iterrows():
            # Determine if the laser is on
            if self.df["laser_status"][index] == 0:
                off_count += 1

        return off_count

    def plot(self, show_off: bool):
        """
        Create a plot of the layer, give the option to show when laser was on/off
        """
        pass


if __name__ == "__main__":

    filepath = r"C:\Users\Anthony\Documents\Tailored\code\common_monitoring_file\transformed_id-010.csv"

    test = Layer(filepath)

    # test.get_number_events_on()
    # test.get_number_events_off()

    # print(test.get_distance_off())
    # print(test.get_distance_on())

    print(test.get_time_off())
    print(test.get_time_on())
