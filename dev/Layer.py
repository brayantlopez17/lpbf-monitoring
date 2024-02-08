import pandas as pd

class Layer:

    def __init__(self, filepath:str):
        self.df = pd.read_csv(filepath)