import pandas as pd

class ecg_reader:

    def __init__(self, data, time=None, voltage=None):
        self.data = data
        self.time = time
        self.voltage = voltage

    @property
    def voltage(self):
        return self.__voltage

    @voltage.setter
    def voltage(self, voltage):
        df = self.read_csv()
        v = pd.to_numeric(df['Voltage'], errors='coerce')
        self.__voltage = pd.DataFrame(v).interpolate().values.ravel().tolist()

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        df = self.read_csv()
        t = pd.to_numeric(df['Time'], errors='coerce')
        self.__time = pd.DataFrame(t).interpolate().values.ravel().tolist()

    def read_csv(self):
        """
        Reads the csv

        :param self: The ecg_reader object
        :returns df: Dataframe storing time and voltage values
        """

        df = pd.read_csv(self.data, names=['Time', 'Voltage'])
        return df
