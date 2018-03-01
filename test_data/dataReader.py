import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import peakutils

class Reader:

    def __init__(self, data, num_segment, time=None, voltage=None):
        self.data = data
        self.num_segment = num_segment
        self.time = time
        self.voltage = voltage
        self.auto = []
        self.read_csv()
        self.rate_finder()

    def read_csv(self):
        df = pd.read_csv(self.data, names=['Time', 'Voltage'])
        self.time = df['Time'].values
        self.voltage = df['Voltage'].values

    def rate_finder(self):
        total_time = math.ceil(len(self.time))
        segment = total_time//self.num_segment
        # print(total_time)
        # print(segment)

        voltage_mean = np.mean(self.voltage)
        self.voltage = self.voltage - voltage_mean
        diff = []

        for i in range(0, self.num_segment):
            voltage_segment = self.voltage[i*segment:i*segment+segment:1]
            self.auto = np.correlate(voltage_segment, voltage_segment, 'same')
            low = math.ceil(len(self.auto)/2)
            high = len(self.auto)
            self.auto = self.auto[low:high:1]
            indices = peakutils.indexes(self.auto, thres=0.18, min_dist=200)
            sum_time = []
            for j in indices:
                sum_time.append(self.time[j])
            for k in range(len(sum_time)-1):
                diff.append(sum_time[k+1]-sum_time[k])
            # plt.plot(self.auto)
            # plt.plot(indices, [self.auto[j] for j in indices],  'r+')
            # plt.show()
            # blah blah blah
        # print(diff)

        print(60/np.mean(diff))

        # print(voltage_segment)

        # for i in range(0, max_time-1):
        #     for j in range(i*segment, i*segment+segment-1):
        #         v_seg = pd.concat(self.voltage
        #     self.auto.append(self.voltage.autocorr(lag=i))
