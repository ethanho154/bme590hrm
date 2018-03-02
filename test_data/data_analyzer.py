import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import peakutils
from dataReader import Reader

class Analyzer:

    def __init__(self, csv_file, num_segment):
        self.num_segment = num_segment
        self.data = Reader(csv_file)
        self.rate_finder()

    def rate_finder(self):
        total_time = math.ceil(len(self.data.time))
        segment = total_time//self.num_segment
        # print(total_time)
        # print(segment)

        voltage_mean = np.mean(self.data.voltage)
        self.data.voltage = self.data.voltage - voltage_mean
        diff = []

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
                diff.append(sum_time[k+1]-sum_time[k])

        print(60/np.mean(diff))
