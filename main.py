import json
from data_analyzer import ecg_analyzer


def hrm(filename, n):
    """
    Outputs the data acquired by ecg_analyzer to json format

    :param filename: string of filename to be analyzed
    :param n: number of segments csv data will be broken up into
    :returns: json file
    """

    f = ecg_analyzer(filename, n)
    data = {'mean_hr_bpm': f.mean_hr_bpm, 'voltage_extremes':
            f.voltage_extremes, 'duration': f.duration, 'num_beats':
            f.num_beats, 'beats': f.beats.tolist()}
    with open(filename[0:len(filename)-4] + '.json', 'w') as outfile:
        json.dump(data, outfile)
