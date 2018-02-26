import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Reader:

    def __init__(self, data, time=None, voltage=None):
        self.data = data
        self.time = time
        self.voltage = voltage
        self.auto = []
        self.read_csv()

    def read_csv(self):
        df = pd.read_csv(self.data, names=['Time', 'Voltage'])
        self.time = df['Time']
        self.voltage = df['Voltage']
        for i in range(0, len(self.voltage)//2):
            self.auto.append(self.voltage.autocorr(lag=i))
