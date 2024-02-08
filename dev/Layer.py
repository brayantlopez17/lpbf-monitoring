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
        on_count = 0

        # Iterate through the dataframe using indexes
        for index, rows in self.df.iterrows():

            # Defines the old and new values
            old = self.df["shift"][index]
            new = self.df["laser_status"][index]

            # Compares the values to determine if the laser went off-->on
            if old == 0 and new == 1:
                on_count += 1

        print(f"The laser is on {on_count} times.")

    def get_number_events_off(self):
        """
        Number of events on indicates when the laser status changed from
        on --> off
        """
        # Define the shift column to move down one index
        self.df["shift"] = self.df["laser_status"].shift()

        # Define the off_count (Number of times laser_status went on --> off)
        off_count = 0

        # Iterate through the dataframe using indexes
        for index, rows in self.df.iterrows():

            # Defines the old and new values
            old = self.df["shift"][index]
            new = self.df["laser_status"][index]

            # Compares the values to determine if the laser went on-->off
            if old == 1 and new == 0:
                off_count += 1

        print(f"The laser is off {off_count} times.")

    def get_distance_on(self):
        """
        Indicates the total distance when the laser was ON
        """
        # Define the shift, x_shift and y_shift columns that moves the index down 1
        self.df["shift"] = self.df["laser_status"].shift()
        self.df["x_shift"] = self.df["x"].shift()
        self.df["y_shift"] = self.df["y"].shift()

        # Define distance_off
        distance_on = 0

        # iterate through the data frame
        for index, rows in self.df.iterrows():

            # Defines the old and new values
            old = self.df["shift"][index]
            new = self.df["laser_status"][index]

            # Determines if the laser is on
            if (old == 1 and new == 1) or (old == 0 and new == 1):
                # Determine the values of x and y by calculating the distance between the new point and old point
                x = self.df["x"][index] - self.df["x_shift"][index]
                y = self.df["y"][index] - self.df["y_shift"][index]

                # Calculate the length between the two points (Pythag Theorem)
                len = np.sqrt(x ** 2 + y ** 2)

                # Add length to dataframe and add to the distance_on
                self.df.loc[index, "length"] = len
                distance_on += len

        print(f"Distance the laser was on: {distance_on}")

    def get_distance_off(self):
        """
        Indicates the total distance when the laser was off
        """
        # Define the shift, x_shift and y_shift columns that moves the index down 1
        self.df["shift"] = self.df["laser_status"].shift()
        self.df["x_shift"] = self.df["x"].shift()
        self.df["y_shift"] = self.df["y"].shift()

        # Define distance_off
        distance_off = 0

        # iterate through the data frame
        for index, rows in self.df.iterrows():

            # Defines the old and new values
            old = self.df["shift"][index]
            new = self.df["laser_status"][index]

            # Determines if the laser is off
            if (old == 0 and new == 0) or (old == 1 and new == 0):
                # Determine the values of x and y by calculating the distance between the new point and old point
                x = self.df["x"][index] - self.df["x_shift"][index]
                y = self.df["y"][index] - self.df["y_shift"][index]

                # Calculate the length between the two points (Pythag Theorem)
                len = np.sqrt(x ** 2 + y ** 2)

                # Add length to dataframe and add to the distance_off
                self.df.loc[index, "length"] = len
                distance_off += len

        print(f"Distance the laser was off: {distance_off}")

    def get_time_on(self):
        """
        Indicates the total time that the laser was on
        """
        # Define shift and time shiftcolumn that moves index down one
        self.df["shift"] = self.df["laser_status"].shift()
        self.df["t_shift"] = self.df["t"].shift()

        # Define variable time_on
        time_on = 0

        # Iterate through the data frame
        for index, rows in self.df.iterrows():
            old = self.df["shift"][index]
            new = self.df["laser_status"][index]

            # Determine if the laser is on
            if (old == 1 and new == 1) or (old == 0 and new == 1):

                # Calculate the elapsed time between the points
                time = self.df["t"][index]-self.df["t_shift"][index]
                # Add to time_on
                time_on += time

        print(f"Laser time on is: {time_on}")

    def get_time_off(self):
        """
        Indicates the total time that the laser was off
        """
        # Define shift column that moves index down one
        self.df["shift"] = self.df["laser_status"].shift()
        self.df["t_shift"] = self.df["t"].shift()

        # Define variable time_off
        time_off = 0

        # Iterate through the data frame
        for index, rows in self.df.iterrows():
            old = self.df["shift"][index]
            new = self.df["laser_status"][index]

            # Determine if the laser is off
            if (old == 0 and new == 0) or (old == 1 and new == 0):

                # Calculate the elapsed time between the points
                time = self.df["t"][index]-self.df["t_shift"][index]
                # Add to time_off
                time_off += time

        print(f"Laser time off is: {time_off}")

    def plot(self, show_off: bool):
        """
        Create a plot of the layer, give the option to show when laser was on/off
        """
        pass


if __name__ == "__main__":

    filepath = r"C:\Users\Anthony\Documents\Tailored\code\common_monitoring_file\transformed_id-001.csv"

    test = Layer(filepath)

    test.get_number_events_on()
    test.get_number_events_off()

    test.get_distance_off()
    test.get_distance_on()

    test.get_time_off()
    test.get_time_on()
