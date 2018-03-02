import pandas as pd

class ecg_reader:

    def __init__(self, data, time=None, voltage=None):
        self.data = data
        self.time = time
        self.voltage = voltage
        self.read_csv()

    def read_csv(self):
        df = pd.read_csv(self.data, names=['Time', 'Voltage'])
        self.time = df['Time'].values
        self.voltage = df['Voltage'].values
