import matplotlib.pyplot as plt
import math
import numpy as np
import peakutils
from data_reader import ecg_reader

class ecg_analyzer:

    def __init__(self, csv_file, num_segment, mean_hr_bpm = None,
                 voltage_extremes = None, duration = None, num_beats = None,
                 beats = None):
        self.csv_file = csv_file
        self.num_segment = num_segment
        self.data = ecg_reader(self.csv_file)
        self.num_segments = num_segment
        self.mean_hr_bpm = mean_hr_bpm
        self.voltage_extremes = voltage_extremes
        self.duration = duration
        self.num_beats = num_beats
        self.beats = beats

    @property
    def num_segment(self):
        return self.__num_segment

    @num_segment.setter
    def num_segment(self, num_segment):
        if num_segment < 0:
            self.__num_segment = -num_segment
        else:
            self.__num_segment = num_segment

    @property
    def voltage_extremes(self):
        return self.__voltage_extremes

    @voltage_extremes.setter
    def voltage_extremes(self, voltage_extremes):
        v_min = np.min(self.data.voltage)
        v_max = np.max(self.data.voltage)
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
        mean_diff = self.rate_finder()
        self.__mean_hr_bpm = 60/mean_diff

    @property
    def num_beats(self):
        return self.__num_beats

    @num_beats.setter
    def num_beats(self, num_beats):
        mean_diff = self.rate_finder()
        max_time = np.max(self.data.time)
        self.__num_beats = math.floor(mean_diff*max_time)

    @property
    def beats(self):
        return self.__beats

    @beats.setter
    def beats(self, beats):
        mean_diff = self.rate_finder()
        segment = self.segment_finder()
        v_norm = self.v_normalize()
        voltage_segment = v_norm[0:segment:1]
        indices = self.autocorr(voltage_segment)
        self.__beats = [self.data.time[indices[0]]]
        j = 0
        while self.__beats[len(self.__beats)-1]<self.duration:
            self.__beats.append(self.data.time[indices[0]+math.floor(j*mean_diff)])
            j += 1
        self.__beats = np.asarray(self.__beats)

    def segment_finder(self):
        total_time = math.ceil(len(self.data.time))
        segment = total_time//self.num_segment
        return segment

    def v_normalize(self):
        v_mean = np.mean(self.data.voltage)
        v_norm = self.data.voltage - v_mean
        return v_norm

    def rate_finder(self):
        """
        This method uses autocorrelation to find the period for patterns in the
        ECG data. The user specifies how many segments the data will be broken
        down into and the period in each segment is found and averaged to
        give an estimate of often a heartbeat occurs in the data.

        :param self: The data_analyzer object
        :returns:

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
        auto = []
        auto = np.correlate(v, v, 'same')
        low = math.ceil(len(auto)/2)
        high = len(auto)
        auto = auto[low:high:1]
        indices = peakutils.indexes(auto, thres=0.18, min_dist=200)
        return indices
