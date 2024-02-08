"""
This class allows to read and parse the dat files from the Renishaw machines
into a common monitoring file csv.
"""

# Built-in
import struct
import os
import configparser

import numpy as np
# Libs
import pandas as pd


__author__ = 'Brayant Lopez'
__copyright__ = 'Copyright 2023, Tailored Alloys'
__license__ = 'MIT'
__version__ = '0.2.2'

# Global Variables
config = configparser.ConfigParser()
config.read("config.ini")

FREQUENCY = int(config['Renishaw']['frequency'])
OFFSET = int(config['Renishaw']['offset'])


class RenishawRawFileReader():

    def __init__(self, filepath:str, commanded:bool = True):
        self._filepath = filepath.replace("\\", "/")
        self._file = open(self._filepath, "rb")
        self._filesize = os.stat(self._filepath).st_size
        self._headerbytes = 84                                          # number of bytes in the header
        self._frequency = 10                                            # monitoring frequency
        self.offset = OFFSET                                            # sensors bit offsets

        self._laser_number = self._read_laser_number()
        self._build_id = self._read_build_id()
        self._timestamp = self._read_timestamp()

        self._datalines = self._read_datalines_number()
        self.df = self._construct_dataframe(commanded=True)


        self._fix_offset()
        self._trim_values()


    def __str__(self):
        return f"Filepath: {self._filepath}/nFile size: {self._filesize} " \
               f"bytes/nLaser number: {self._laser_number}/nBuild ID: " \
               f"{self._build_id}/nTimestamp: {self._timestamp}/nData lines: {self._datalines}"

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

    def _read_laser_number(self) -> int:
        """
        Laser number used. This value
        poistion: 4th byte
        size: 2 bytes (unsigned character 'B')
        :return: number of laser
        """
        return self.__read_bytes_at(4, 1, 'B')

    def _read_build_id(self):
        """
        Build ID for the file.
        Byte position: 14th
        size: 4 bytes (unsigned int 'I')
        :return: build id
        """
        return self.__read_bytes_at(14, 4, 'I')

    def _read_datalines_number(self):
        """
        Number of data lines in the file.
        Byte position: 28th
        size: 4 bytes (signed int 'i')
        :return: number of data lines
        """
        return self.__read_bytes_at(28, 4, 'i')

    def _read_timestamp(self):
        """
        Time stamp for the file.
        Byte position: 6th
        size: 8 bytes (signed long long 'q')
        :return: time stamp
        """
        return self.__read_bytes_at(6, 8, 'q')

    def _construct_dataframe(self, commanded:bool = True):
        """
        Dataframe that contains the data from the file. If the commanded is true, then the dataframe contains the
        commanded position values. If false, then the dataframe contains the actual position values.
        :return: pandas dataframe
        """
        t, x_pos, y_pos, z_pos = [], [], [], []
        x0, y0, z0, Ls = [], [], [], []
        Lp, Mvw, Pvw, Lvw = [], [], [], []
        fill8, fill9 = [], []

        for i in range(self._datalines):
            t.append(self._frequency*i)
            x_pos.append(self.__read_bytes_at(84 + (i * 26), 2, 'H'))
            y_pos.append(self.__read_bytes_at(86 + (i * 26), 2, 'H'))
            z_pos.append(self.__read_bytes_at(88 + (i * 26), 2, 'H'))
            x0.append(self.__read_bytes_at(90 + (i * 26), 2, 'H'))
            y0.append(self.__read_bytes_at(92 + (i * 26), 2, 'H'))
            z0.append(self.__read_bytes_at(94 + (i * 26), 2, 'H'))
            Ls.append(1 if int(self.__read_bytes_at(96 + (i * 26), 2, 'H') > 0) else 0)
            Lp.append(self.__read_bytes_at(98 + (i * 26), 2, 'H'))
            Mvw.append(self.__read_bytes_at(100 + (i * 26), 2, 'H'))
            Pvw.append(self.__read_bytes_at(102 + (i * 26), 2, 'H'))
            Lvw.append(self.__read_bytes_at(104 + (i * 26), 2, 'H'))
            fill8.append(self.__read_bytes_at(106 + (i * 26), 2, 'H'))
            fill9.append(self.__read_bytes_at(108 + (i * 26), 2, 'H'))

        if commanded:
            df = pd.DataFrame({'t': t, "x": x_pos, "y": y_pos, "z": z_pos, 'power': Lp, 'laser_status': Ls, 'Mvw': Mvw,
                               'PVw': Pvw, 'LVw': Lvw, 'Fill8': fill8, 'Fill9': fill9})

            # df = self._fix_offset(df)

        else:
            df = pd.DataFrame({'t': t, "x": x0, "y": y0, "z": z0, 'power': Lp, 'laser_status': Ls, 'MVw': Mvw, 'PVw': Pvw,
                               'LVw': Lvw, 'Fill8': fill8, 'Fill9': fill9})
        return df

    def _fix_offset(self):
        if OFFSET > 0:
            self.df['x'] = np.roll(np.array(self.df["x"]), OFFSET)
            self.df['y'] = np.roll(np.array(self.df["y"]), OFFSET)

    def _trim_values(self):
        msk_lst = self.df.index[self.df['laser_status'] == 1].tolist()
        i, j = msk_lst[0], msk_lst[-1]
        self._df = self.df[i:j]

    @property
    def laser_number(self): return self._laser_number

    @property
    def build_id(self): return self._build_id

    @property
    def timestamp(self): return self._timestamp

    def get_dataframe(self):
        return self.df

    def write_to_csv(self, dir: str):
        output_dir = dir.replace("\\", "/")
        outputfile = os.path.join(output_dir, f"ren-id-{self._build_id}_lsr{self._laser_number}.csv")
        self.df.to_csv(outputfile, index=False)

    def write_to_pickle(self):
        self.df.to_pickle("test.pkl")

    def write_to_txt(self):
        with open("test.txt", 'w') as file:
            # file.write(f"#timestamp: {self._timestamp}\n")
            file.write("t\tx'\ty'\tz'\tx\ty\tz\tL_s\tL_p\tMVw\tPVw\tLVw\tFill8\tFill9\n")
            for i in range(self._datalines-1):
                t = self._frequency*i
                x = self.__read_bytes_at(84 + (i * 26), 2, 'H')
                y = self.__read_bytes_at(86 + (i * 26), 2, 'H')
                z = self.__read_bytes_at(88 + (i * 26), 2, 'H')
                x0 = self.__read_bytes_at(90 + (i * 26), 2, 'H')
                y0 = self.__read_bytes_at(92 + (i * 26), 2, 'H')
                z0 = self.__read_bytes_at(94 + (i * 26), 2, 'H')
                Ls = self.__read_bytes_at(96 + (i * 26), 2, 'H')
                Lp = self.__read_bytes_at(98 + (i * 26), 2, 'H')
                Mvw = self.__read_bytes_at(100 + (i * 26), 2, 'H')
                Pvw = self.__read_bytes_at(102 + (i * 26), 2, 'H')
                Lvw = self.__read_bytes_at(104 + (i * 26), 2, 'H')
                f8 = self.__read_bytes_at(106 + (i * 26), 2, 'H')
                f9 = self.__read_bytes_at(108 + (i * 26), 2, 'H')
                file.write(f"{t}\t{x}\t{y}\t{z}\t{x0}\t{y0}\t{z0}\t{Ls}\t{Lp}\t{Mvw}\t{Pvw}\t{Lvw}\t{f8}\t{f9}\n")
            file.close()

    def to_h5(self, output_file, layer_num: str):
        layer = f"layer_{layer_num}"
        self._df.to_hdf(output_file, key=layer, format="table", data_columns=True, index=False)


if __name__ == "__main__":
    in_dir = r"C:\Users\braya\HT_Test\MonitoringData\UTEP 45\UTEP 45\dat files"
    out_dir = r"C:\Users\braya\HT_Test\MonitoringData\UTEP 45\UTEP 45\dat files\transformed"

    filepath = r"C:\Users\braya\HT_Test\MonitoringData\UTEP 45\UTEP 45\dat files\AMPM_324_L1_100K_2023-06-08_11-07-33.dat"
    obj = RenishawRawFileReader(filepath)
    obj.write_to_csv(out_dir)



