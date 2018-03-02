import pandas as pd
import logging
logging.basicConfig(filename='log.txt', level=logging.DEBUG)


class ecg_reader:

    """
    The ecg_reader object reads data from csv files and parses the time and
    voltage data

    Attributes:
        :data (str): String containing filename to be read

        :time (list):

        :voltage (list):

    """

    def __init__(self, data, time=None, voltage=None):
        self.data = data
        self.data_check()
        logging.info("csv file succesfully read")
        self.time = time
        self.voltage = voltage
        logging.info("time and voltage data obtained")

    @property
    def voltage(self):
        return self.__voltage

    @voltage.setter
    def voltage(self, voltage):
        """
        converts voltage dataframe col to list

        :params self: ecg_reader object

        :returns: voltage list from data
        """

        df = self.read_csv()
        v = pd.to_numeric(df['Voltage'], errors='coerce')
        self.__voltage = pd.DataFrame(v).interpolate().values.ravel().tolist()

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        """
        converts time dataframe col to list

        :params self: ecg_reader object

        :returns: time list from data
        """
        df = self.read_csv()
        t = pd.to_numeric(df['Time'], errors='coerce')
        self.__time = pd.DataFrame(t).interpolate().values.ravel().tolist()

    def read_csv(self):
        """
        Reads the csv

        :param self: The ecg_reader object

        :returns: df dataframe for storing time and voltage values
        """

        df = pd.read_csv(self.data, names=['Time', 'Voltage'])
        return df

    def data_check(self):
        """
        Makes sure that filename is a valid input

        :param self: ecg_reader object

        :raises TypeError: data must be a string
        """

        logging.warning("Incorrect data type used")
        if isinstance(self.data, str) is False:
            raise TypeError('Filename not a string')
