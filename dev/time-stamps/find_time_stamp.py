import struct
import datetime
import csv

class time_stamp_finder:

    def __init__(self,filepath):
        self._filepath = filepath
        self._file = open(self._filepath, "rb")

    def _read_bytes_at(self, i: int, r: int, format: str):
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

    def read_time_stamps(self, i:int):
        time_stamp_bytes = self._read_bytes_at(i,4,'I')
        print(time_stamp_bytes)
        return datetime.datetime.fromtimestamp(time_stamp_bytes)

    def read_time_stamps_as_long(self, index:int):
        time_stamp_bytes = self._read_bytes_at(index,4,'L')
        print(time_stamp_bytes)
        return datetime.datetime.fromtimestamp(time_stamp_bytes)

    def read_time_stamps_as_unsigned_long_long(self, index:int):
        time_stamp_bytes = self._read_bytes_at(index,8,'Q')
        return time_stamp_bytes


if __name__ == "__main__":
    filepath = "C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/dat files/AMPM_1_L1_100K_2023-06-08_09-22-44.dat"
    filepath2 = "C:/Users/braya/HT_Test/MonitoringData/UTEP 45/UTEP 45/dat files/AMPM_2_L1_100K_2023-06-08_09-22-57.dat"

    obj = time_stamp_finder(filepath)
    obj2 = time_stamp_finder(filepath2)


    stamps1 = []
    stamps2 = []
    index = []
    for i in range(4,75):
        index.append(i)
        stamps1.append(obj.read_time_stamps_as_unsigned_long_long(i))
        stamps2.append(obj2.read_time_stamps_as_unsigned_long_long(i))

    lst = zip(index, stamps1, stamps2)

    with open("reader time_stamps-usigned-longlong.csv", 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(['index','timestamp 1', 'timestamp 2'])
        wr.writerows(lst)
