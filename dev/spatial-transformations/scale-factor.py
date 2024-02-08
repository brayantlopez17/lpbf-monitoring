import os.path
from tqdm import tqdm
import pandas as pd


def create_output_dir(input_dir:str):
    output_dir = os.path.join(input_dir, "scaled")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    return output_dir


def create_output_dir_transformed(input_dir:str):
    output_dir = os.path.join(input_dir, "transformed")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    return output_dir


def create_output_filename(filename:str):
    file_name = filename[:filename.rfind(".")]
    output_file = f"{file_name}_scaled.csv"
    return output_file


def create_output_filename_translated(filename:str):
    file_name = filename[:filename.rfind(".")]
    output_file = f"{file_name}_transformed.csv"
    return output_file


def scale_files(input_dir, scale):
    output_dir = create_output_dir(input_dir)
    for file in tqdm(os.listdir(input_dir), desc="scaling files", ncols=100, colour="green"):
        if file.endswith(".csv"):
            input_file = os.path.join(input_dir, file)
            output_file = create_output_filename(file)
            output_filepath = os.path.join(output_dir, output_file)
            df = pd.read_csv(input_file)
            df['x'] = df['x'] / scale
            df['y'] = df['y'] / scale
            df.to_csv(output_filepath, index=False)

def translate_files(input_dir, dx ,dy):
    output_dir = create_output_dir_transformed(input_dir)
    for file in tqdm(os.listdir(input_dir), desc="scaling files", ncols=100, colour="green"):
        if file.endswith(".csv"):
            input_file = os.path.join(input_dir, file)
            output_file = create_output_filename_translated(file)
            output_filepath = os.path.join(output_dir, output_file)
            df = pd.read_csv(input_file)
            df['x'] = df['x'] - dx
            df['y'] = df['y'] - dy
            df.to_csv(output_filepath, index=False)

if __name__ == "__main__":
    input_dir = r"C:\Users\braya\HT_Test\MonitoringData\UTEP 45\UTEP 45\dat files\transformed\scaled"

    translate_files(input_dir, dx=277.843, dy=50.261)
