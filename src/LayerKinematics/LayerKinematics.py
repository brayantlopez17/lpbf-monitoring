import pandas as pd
import numpy as np
import json


class LayerKinematics:
    """
    This class will take a file from the common monitoring file format and
    calculate the time and distance the laser is on and off.
    public methods:
        - get_values()->dict: returns a dictionary with the time and distance values
    """

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df = pd.read_csv(self.filepath)

        self.df['length'] = np.sqrt(self.df["x"].diff() ** 2 + self.df["y"].diff() ** 2)
        self.df['event'] = self.df['laser_status'].diff()
        self.df['event'] = self.df['event'].fillna(0)
        self.df['event'] = self.df['event'].astype(int)

        self.time_on = float()
        self.time_off = float()
        self.no_events = int()
        self.no_events_off = int()
        self.distance_on = float()
        self.distance_off = float()

        self._calculate_time_distance_on()
        self._calculate_time_distance_off()
        self._retrieve_no_events()
        self._retrieve_no_events_off()

        self.summary = {
            'time on': self.time_on,
            'time off': self.time_off,
            'distance on': self.distance_on,
            'distance off': self.distance_off,
            'total distance': self.distance_on + self.distance_off,
            'total time': self.time_on + self.time_off,
            'number events': self.no_events,
            'number events off': self.no_events_off
        }

    def _calculate_time_distance_on(self):
        df_on = self.df[self.df['laser_status'] == 1]
        self.distance_on = df_on['length'].sum()
        self.time_on = len(df_on)

    def _calculate_time_distance_off(self):
        df_off = self.df[self.df['laser_status'] == 0]
        self.distance_off = df_off['length'].sum()
        self.time_off = len(df_off)

    def _retrieve_no_events(self):
        df = self.df[self.df['event'] == 1]
        self.no_events = len(df)

    def _retrieve_no_events_off(self):
        df = self.df[self.df['event'] == -1]
        self.no_events_off = len(df)

    def get_values(self):
        return self.summary

    def to_json(self, output_file: str):
        with open(output_file, 'w') as fp:
            json.dump(self.summary, fp)


if __name__ == "__main__":
    filepath = r"C:\Users\Brayant_TA\TailoredAlloys\Test_Data\MonitoringData\UTEP 45\UTEP 45\common_monitoring_file\transformed_id-042.csv"
    obj = LayerKinematics(filepath)

    obj.to_json('answers.json')
