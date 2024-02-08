"""
Module to take the directory of the monitoring files and
parse each file into the common monitorium file format.
"""

# Built-in/Generic Imports
import struct
import os

# Local Modules
from mpmReader import SLMReader
from renishawReader import RenishawRawFileReader


__author__ = 'Brayant Lopez'
__copyright__ = 'Copyright 2023, Tailored Alloys'
__license__ = 'MIT'
__version__ = '0.0.1'

# Global Variables
SLM_EXT = '.mpm'
REN_EXT = '.dat'
EOS_EXT = '.h5'
ACO_EXT = '.pcd'


def create_new_directory(input_dir:str) -> str:
    """
    :param input_dir: directory that contains the monitoring files
    :return: the new directory path where the parsed monitoring file will be located
    """
    new_dir = os.path.join(input_dir, "processed")
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    return new_dir


# def parse_files_into_new_dir(input_dir:str, machine:str) -> None:
#     """
#     :param input_dir: directory that contains the monitoring files
#     :param machine: type of files from the machine
#     :return: It creates all the csv files from
#     """
#     extension = str()
#     if machine.lower() == 'slm':
#         extension = SLM_EXT
#     elif machine.lower() == 'renishaw':
#         extension = REN_EXT
#     elif machine.lower() == 'eos':
#         extension = EOS_EXT
#     elif machine.lower() == 'aconity':
#         extension = ACO_EXT
#     for file in os.listdir(input_dir):
#         if file.endswith(extension):

