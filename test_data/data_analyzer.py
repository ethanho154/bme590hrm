import matplotlib.pyplot as plt
import math
import numpy as np
import peakutils
from data_reader import ecg_reader

class ecg_analyzer:

    def __init__(self, csv_file, num_segment, diff = [], mean_hr_bpm = None,
                 voltage_extremes = None, duration = None, num_beats = None,
                 beats = None):
        self.csv_file = csv_file
        self.num_segments = num_segment
        self.diff = diff
        self.mean_hr_bpm = mean_hr_bpm
        self.voltage_extremes = voltage_extremes
        self.duration = duration
        self.num_beats = num_beats
        self.beats = beats
        self.num_segment = num_segment
        self.data = ecg_reader(self.csv_file)
        self.find_voltage_extremes()
        self.find_duration()
        self.rate_finder()
        self.find_mean_hr_data()

    def rate_finder(self):
        """
        This method uses autocorrelation to find the period for patterns in the
        ECG data. The user specifies how many segments the data will be broken
        down into and the period in each segment is found and averaged to
        give an estimate of often a heartbeat occurs in the data.

        :param self: The data_analyzer object
        :returns:

        """
        total_time = math.ceil(len(self.data.time))
        segment = total_time//self.num_segment

        voltage_mean = np.mean(self.data.voltage)
        self.data.voltage = self.data.voltage - voltage_mean

        for i in range(0, self.num_segment):
            auto = []
            voltage_segment = self.data.voltage[i*segment:i*segment+segment:1]
            time_segment = self.data.time[i*segment:i*segment+segment:1]
            sum_time = []
            sum_time.append(time_segment[0])
            auto = np.correlate(voltage_segment, voltage_segment, 'same')
            low = math.ceil(len(auto)/2)
            high = len(auto)
            auto = auto[low:high:1]
            indices = peakutils.indexes(auto, thres=0.18, min_dist=200)
            for j in indices:
                sum_time.append(time_segment[j])
            for k in range(len(sum_time)-1):
                self.diff.append(sum_time[k+1]-sum_time[k])

    def autocorr(self):
        pass

    def find_voltage_extremes(self):
        v_min = np.min(self.data.voltage)
        v_max = np.max(self.data.voltage)
        self.voltage_extremes = (v_min, v_max)

    def find_duration(self):
        self.duration = np.max(self.data.time)

    def find_mean_hr_data(self):
        total_time = math.ceil(len(self.data.time))
        segment = total_time//self.num_segment
        mean_diff = np.mean(self.diff)
        self.mean_hr_bpm = 60/mean_diff
        self.num_beats = math.floor(self.duration*mean_diff)
        voltage_segment = self.data.voltage[0:segment:1]
        auto = np.correlate(voltage_segment, voltage_segment, 'same')
        low = math.ceil(len(auto)/2)
        high = len(auto)
        auto = auto[low:high:1]
        indices = peakutils.indexes(auto, thres=0.18, min_dist=200)
        j = 0
        while self.beats[len(self.beats)-1]<self.duration:
            np.append(self.beats, time[indices[0]+i*mean_diff])
            j += 1
