import json
from data_analyzer import ecg_analyzer

def hrm(filename):
    f = ecg_analyzer(filename, 5)
    data = {'mean_hr_bpm': f.mean_hr_bpm, 'voltage_extremes': f.voltage_extremes,
            'duration': f.duration, 'num_beats': f.num_beats,
            'beats': f.beats.tolist()}
    with open('filename.json', 'w') as outfile:
        json.dump(data, outfile)
