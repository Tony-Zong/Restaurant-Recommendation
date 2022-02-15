import pandas as pd
def load(file_name):
    return pd.read_pickle(file_name)