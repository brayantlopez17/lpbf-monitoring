"""
This class allows to read and parse the mpm files from the SLM machines
into a common monitoring file csv.
"""

# Built-in/Generic Imports
import struct
import os
import configparser
from tqdm import tqdm

# Libs
import pandas as pd
import numpy as np

__author__ = 'Brayant Lopez'
__copyright__ = 'Copyright 2023, Tailored Alloys'
__license__ = 'MIT'
__version__ = '0.2.2'

# Global Variables
config = configparser.ConfigParser()
config.read("config.ini")

FREQUENCY = int(config['SLM']['frequency'])
OFFSET = int(config['SLM']['offset'])
LAYER_THICKNESS = round(float(config['SLM']['layer_thickness']), 3)


class SLMReader:
    def __init__(self, filepath: str, auto_parse=False):
        """
        The file is ingested and read as a binary file.
        The monitoring file has a header with metadata:
            - filesize: number of bytes in the file
            - layer number: number of layer
            - header_offset: number of bytes to the data entries
            - datalines: number of data lines

        The layer number is used to compute the height in the Z-axis with the layer thickness
        """

        self._filepath = filepath.replace("\\", "/")
        self._directory = filepath[:filepath.rfind("/")]
        self._file = open(self._filepath, "rb")  # read file as a binary
        self._filesize = int(os.stat(self._filepath).st_size)  # number of bytes in the file
        self._layer_number = self._get_layer_num()
        self.outfilepath = self._get_output_file()  # output filepath

        self._header_offset = self._read_header_offset()  # number of  byte indexes in header
        self._datalines = int((self._filesize - self._header_offset) / 12)  # number of datalines

        self._frequency = FREQUENCY  # monitoring frequency

        self._z_coordinate = self._get_z_coordinate()  # z coordinate value in microns
        self._df = self._construct_dataframe()  # dataframe

        self._offset = OFFSET
        self._trim_values()

        self._fix_offset()

        self._auto_csv() if auto_parse else None

    ###################################################################################################
    #   INGESTING
    ###################################################################################################

    def __read_bytes_at(self, i: int, r: int, format: str):
        """
        Reads the bytes of the file at the position i,
        :param i: index position in the file
        :param r: range of bytes read
        :param format: the format in the struct library
        :return: return a python int data value
        """
        self._file.seek(i, 0)
        var = self._file.read(r)
        return int(struct.unpack(format, var)[0])

    def _read_laser_attributes(self, i):
        """
        Read the laser power and laser_status, if the laser status is euqal to zero, return 0,0.
        """
        short = self.__read_bytes_at(i, 2, 'H')
        if short == 0:
            return 0, 0

        num_bin = bin(short)
        if len(num_bin) == 17:
            laser_stat = 0
            power_stat = 0
        else:
            laser_stat = 1
            power_stat = self.__binary_to_decimal(num_bin[5:])
        return laser_stat, power_stat

    def __binary_to_decimal(self, n):
        return int(n, 2)

    def _read_header_offset(self) -> int:
        """
        Header offset. This value
        poistion: 13th byte
        size: 4 bytes (signed int 'B')
        :return: number of bytes for header offset
        """
        return self.__read_bytes_at(12, 4, 'i')

    def _construct_dataframe(self):
        """
        Dataframe that contains the values from the .dat file
        :return: pandas dataframe
        """
        t, sensor1, sensor2, power = [], [], [], []
        x_pos, y_pos, z_pos, laser, fill1 = [], [], [], [], []

        for i in range(self._datalines):
            t.append(self._frequency * i)
            sensor1.append(self.__read_bytes_at(self._header_offset + (i * 12), 2, 'H'))
            sensor2.append(self.__read_bytes_at(self._header_offset + (i * 12) + 2, 2, 'H'))
            x_pos.append(self.__read_bytes_at(self._header_offset + (i * 12) + 4, 2, 'H'))
            y_pos.append(self.__read_bytes_at(self._header_offset + (i * 12) + 6, 2, 'H'))
            z_pos.append(self._z_coordinate)
            l, p = self._read_laser_attributes(self._header_offset + (i * 12) + 8)
            laser.append(l)
            power.append(p)
            fill1.append(self.__read_bytes_at(self._header_offset + (i * 12) + 10, 2, 'H'))

        df = pd.DataFrame(
            {"t": t, "x": x_pos, "y": y_pos, "z": z_pos, "power": power, "laser_status": laser, "sensor1": sensor1,
             "sensor2": sensor2, "Fill1": fill1})
        return df

    def _get_z_coordinate(self):
        """
        Returns the z coordinate based on the layer number and the layer thickness
        """
        return round(float(self._layer_number * LAYER_THICKNESS), 3)

    def _get_layer_num(self):
        locator = [i for i in range(len(self._filepath)) if self._filepath.startswith("_", i)]
        i, j = locator[-2], locator[-1]
        return int(self._filepath[i + 1:j])

    def _get_output_file(self):
        """
        Function to create the output file. The method starts by creating the new directory. The output file
        takes the layer number by finding the "_" character in the filepath string.
        Returns the filepath to the output csv and populates the layer number.
        """
        self._create_parsed_dir()
        locator = [i for i in range(len(self._filepath)) if self._filepath.startswith("_", i)]
        i, j = locator[-2], locator[-1]
        self._layer_number = int(self._filepath[i + 1:j])
        return f"{self._directory}/data/slm-id_{self._filepath[i + 1:j]}_l1.csv"

    def _create_parsed_dir(self):
        if os.path.exists(f"{self._directory}/data"):
            return
        else:
            os.mkdir(f"{self._directory}/data")

    ###################################################################################################
    #   CURATING
    ###################################################################################################
    def _fix_offset(self):
        if OFFSET > 0:
            t = self._df['t']
            x = np.roll(np.array(self._df["x"]), OFFSET)
            y = np.roll(np.array(self._df["y"]), OFFSET)
            p = np.array(self._df["power"])
            laser_status = np.array(self._df["laser_status"])
            sensor1 = np.array(self._df["sensor1"])
            sensor2 = np.array(self._df["sensor2"])
            fill1 = np.array(self._df["fill1"])

            df2 = pd.DataFrame(
                {'t': t, "x": x, "y": y, "power": p, "laser_status": laser_status, "sensor1": sensor1,
                 "sensor2": sensor2,
                 "fill1": fill1})

            self._df = df2

    def _trim_values(self):
        msk_lst = self._df.index[self._df['laser_status'] == 1].tolist()
        i, j = msk_lst[0], msk_lst[-1]
        self._df = self._df[i:j]

    def _auto_csv(self):
        """
        Converts the .mpm file into a .csv file
        :return: None
        """
        self._df.to_csv(self.outfilepath, index=False)

    ###################################################################################################
    #   Public Methods
    ###################################################################################################
    def to_csv(self, output_filepath):
        self._df.to_csv(output_filepath, index=False)

    def to_h5(self, output_file, layer_num: str):
        layer = f"layer_{layer_num}"
        self._df.to_hdf(output_file, key=layer, format="table", data_columns=True, index=False)

    def view_monitoring_file(self):
        print(self._df.head(10))


if __name__ == "__main__":
    dir_ls = r"C:\Users\braya\HT_Test\MonitoringData\UTEP49_F\UTEP49_F\MPM"
    for file in tqdm(os.listdir(dir_ls), desc="Converting MPM files",colour="green", ncols=100):
        in_file = f"{dir_ls}/{file}"
        obj = SLMReader(in_file)



