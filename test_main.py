import pytest
import json


def test_hrm():
    """
    This unit test will test whether or not main can write to json files
    """

    from main import hrm
    mean_hr_bpm = 74.44784514848209
    voltage_extremes = [-0.68, 1.05]
    duration = 27.775
    num_beats = 22
    beats = [0.8140000000000001, 1.6199333333333334, 2.425866666666667,
              3.2318000000000002, 4.037733333333334, 4.8436666666666675,
              5.6496, 6.455533333333333, 7.261466666666667,
              8.067400000000001, 8.873333333333335, 9.679266666666667,
              10.4852, 11.291133333333335, 12.097066666666667,
              12.903, 13.708933333333334, 14.514866666666668,
              15.320800000000002, 16.126733333333334, 16.93266666666667,
              17.7386, 18.544533333333334, 19.35046666666667, 20.1564,
              20.962333333333333, 21.76826666666667, 22.5742,
              23.380133333333333, 24.18606666666667, 24.992,
              25.797933333333336, 26.60386666666667, 27.4098,
              28.215733333333336]

    hrm('test_data1.csv', 5)
    data = json.load(open('test_data1.json'))
    assert data["mean_hr_bpm"] == mean_hr_bpm
    assert data["voltage_extremes"] == voltage_extremes
    assert data["duration"] == duration
    assert data["num_beats"] == num_beats
    assert data["beats"] == pytest.approx(beats, 0.5)
