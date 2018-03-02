import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import peakutils

class Reader:

    def __init__(self, data, time=None, voltage=None):
        self.data = data
        self.time = time
        self.voltage = voltage
        self.read_csv()

    def read_csv(self):
        df = pd.read_csv(self.data, names=['Time', 'Voltage'])
        self.time = df['Time'].values
        self.voltage = df['Voltage'].values
