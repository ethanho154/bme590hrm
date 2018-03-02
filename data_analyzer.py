import logging
logging.basicConfig(filename='log.txt', level=logging.DEBUG)
import math
import numpy as np
import peakutils
from data_reader import ecg_reader

class ecg_analyzer:
    """
    The ecg_analyzer object performs calculations on the data from ecg_reader
    and finds various information from it

    Attributes:
        :csv_file (str): String containing filename to be read

        :num_segment (int): Number of segments to break data into

        :data (ecg_reader): Class containing time and voltage data

        :mean_hr_bpm (float): Average heart rate per minute

        :voltage_extremes (tuple): Highest and lowest voltage in data

        :duration (float): ECG time length

        :num_beats (float): Number of beats in ECG

        :beats (np.array): Time of each beat

    """

    def __init__(self, csv_file, num_segment, data = None, mean_hr_bpm = None,
                 voltage_extremes = None, duration = None, num_beats = None,
                 beats = None):
        self.import_modules()
        self.csv_file = csv_file
        self.check_csv_file()
        logging.info("csv file read")
        self.num_segment = num_segment
        self.check_num_seg()
        self.data = data
        logging.info("data initialized")
        self.num_segments = num_segment
        self.mean_hr_bpm = mean_hr_bpm
        self.voltage_extremes = voltage_extremes
        self.duration = duration
        self.num_beats = num_beats
        self.beats = beats
        logging.info("ECG attributes calculated")

    def import_modules(self):
        try:
            import matplotlib.pyplot as plt
        except:
            logging.warning("matplotlib missing")
            raise ImportError("matplotlib not installed")

    def check_csv_file(self):
        """
        Makes sure that filename is a valid input

        :param self: The ecg_analyzer object
        :raises TypeError: Filename must be a string
        """

        logging.warning("Incorrect data type used")
        if isinstance(self.csv_file, str) == False:
            raise TypeError('Filename not a string')

    def check_num_seg(self):
        """
        Makes sure that number of segments is a valid input

        :param self: The ecg_analyzer object
        :raises ValueError: Number of segments needs to be attainable
        """

        logging.warning("Not a usable number")
        if self.num_segment <= 0:
            raise ValueError('Segment must be greater than 0')

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        """
        Initializes ecg_reader object to bring in data to be analyzed

        :param self: The ecg_analyzer object
        :returns: data ecg_reader object
        """

        self.__data = ecg_reader(self.csv_file)

    @property
    def voltage_extremes(self):
        return self.__voltage_extremes

    @voltage_extremes.setter
    def voltage_extremes(self, voltage_extremes):
        """
        Finds max and min voltages in dataset

        :param self: The ecg_analyzer object
        :returns: voltage_extremes tuple containing min and max voltages
        """

        v_min = np.min(self.data.voltage)
        v_max = np.max(self.data.voltage)
        if v_min < -300.0 or v_max > 300.0:
            logging.debug("unusally large voltage values found")
        self.__voltage_extremes = (v_min, v_max)

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, duration):
        self.__duration = np.max(self.data.time)

    @property
    def mean_hr_bpm(self):
        return self.__mean_hr_bpm

    @mean_hr_bpm.setter
    def mean_hr_bpm(self, mean_hr_bpm):
        """
        Uses rate_finder() to estimate average bpm

        :param self: The ecg_analyzer object
        :returns: mean_hr_bpm float approximating mean
        """
        mean_diff = self.rate_finder()
        self.__mean_hr_bpm = 60/mean_diff
        if self.__mean_hr_bpm < 0:
            logging.debug("negative mean_hr_bpm detected, resize segments")

    @property
    def num_beats(self):
        return self.__num_beats

    @num_beats.setter
    def num_beats(self, num_beats):
        """
        Uses rate_finder() and data duration to estimate beats in data

        :param self: The ecg_analyzer object
        :returns: num_beats float approximating number of beats
        """
        mean_diff = self.rate_finder()
        max_time = np.max(self.data.time)
        self.__num_beats = math.floor(mean_diff*max_time)

    @property
    def beats(self):
        return self.__beats

    @beats.setter
    def beats(self, beats):
        """
        Finds first autocorrelation peak and adds on rate_finder peak to peak
        distance to estimate when heartbeats occur

        :param self: The ecg_analyzer object
        :returns: beats numpy array containing all times
        """
        mean_diff = self.rate_finder()
        segment = self.segment_finder()
        v_norm = self.v_normalize()
        voltage_segment = v_norm[0:segment:1]
        indices = self.autocorr(voltage_segment)
        self.__beats = [self.data.time[indices[0]]]
        j = 1
        while self.__beats[len(self.__beats)-1]<self.duration:
            self.__beats.append(self.data.time[indices[0]]+j*mean_diff)
            j += 1
        self.__beats = np.asarray(self.__beats)

    def segment_finder(self):
        """
        Finds segment length based on how many segments user input

        :param self: The ecg_analyzer object
        :returns: segment int for segment length
        """

        total_time = math.ceil(len(self.data.time))
        segment = total_time//self.num_segment
        return segment

    def v_normalize(self):
        """
        Normalizes voltage data for autocorrelation by subtracting mean

        :param self: The ecg_analyzer object
        :returns: v_norm int which is normalized voltage
        """

        v_mean = np.mean(self.data.voltage)
        v_norm = self.data.voltage - v_mean
        return v_norm

    def rate_finder(self):
        """
        Used autocorrelation to find the period for patterns in the
        ECG data. User specifies how many segments data will be broken
        down into and peak to peak index difference is found and averaged
        to give an estimate of how often a heartbeat occurs

        :param self: The ecg_analyzer object
        :returns: mean_diff float about the mean difference in index
        position of all the peaks found via autocorrelation
        """

        diff = []
        segment = self.segment_finder()
        v_norm = self.v_normalize()
        for i in range(0, self.num_segment):
            voltage_segment = v_norm[i*segment:i*segment+segment:1]
            time_segment = self.data.time[i*segment:i*segment+segment:1]
            sum_time = []
            sum_time.append(time_segment[0])
            indices = self.autocorr(voltage_segment)
            for j in indices:
                sum_time.append(time_segment[j])
            for k in range(len(sum_time)-1):
                diff.append(sum_time[k+1]-sum_time[k])
        mean_diff = np.mean(diff)
        return mean_diff

    def autocorr(self, v):
        """
        Performs autocorrelation on segment and rescales

        :param self: The ecg_analyzer object
        :param v: Voltage segment being autocorrelated
        :returns: indices list in which the index are where peaks occur
        """

        auto = []
        auto = np.correlate(v, v, 'same')
        low = math.ceil(len(auto)/2)
        high = len(auto)
        auto = auto[low:high:1]
        indices = peakutils.indexes(auto, thres=0.18, min_dist=200)
        return indices
