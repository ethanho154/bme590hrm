import pytest

def test_ecg_analyzer():
    """
    Tests to see if ecg_analyzer can handle more normal ECG data (test 1) as
    well as special cases (tests 2 and 3)
    """

    from data_analyzer import ecg_analyzer

    test1_expected = [75, [-0.7, 1], 30, 20, [0.814, 1.619, 2.425, 3.231,
                      4.037, 4.843, 5.649, 6.455, 7.26, 8.067, 8.873, 9.679,
                      10.485, 11.291, 12.097, 12.903, 13.708, 14.514, 15.32,
                      16.126, 16.932, 17.738, 18.544, 19.350, 20.1564, 20.962,
                      21.768, 22.574, 23.3801, 24.186, 24.992, 25.797, 26.603,
                      27.409, 28.215]]

    test1 = ecg_analyzer('test_data1.csv', 5)
    assert test1.mean_hr_bpm == pytest.approx(test1_expected[0], 5)
    assert test1.voltage_extremes == pytest.approx(test1_expected[1], 0.25)
    assert test1.duration == pytest.approx(test1_expected[2], 5)
    assert test1.num_beats == pytest.approx(test1_expected[3], 3)
    assert test1.beats == pytest.approx(test1_expected[4], 0.5)

    test30_expected = [70, [-1.7, 5.1], 40, 35, [0.5, 1.375, 2.250, 3.125,
                       4.000, 4.875, 5.750, 6.626, 7.501, 8.376, 9.251, 10.126,
                       11.001, 11.877, 12.752, 13.627, 14.502, 15.377, 16.252,
                       17.128, 18.003, 18.878, 19.753, 20.628, 21.503, 22.378,
                       23.254, 24.129, 25.004, 25.879, 26.754, 27.629, 28.505,
                       29.380, 30.255, 31.130, 32.005, 32.880, 33.756, 34.631,
                       35.506, 36.381, 37.256, 38.131, 39.006, 39.882, 40.757]]

    test30 = ecg_analyzer('test_data30.csv', 5)
    assert test30.mean_hr_bpm == pytest.approx(test30_expected[0], 5)
    assert test30.voltage_extremes == pytest.approx(test30_expected[1], 0.25)
    assert test30.duration == pytest.approx(test30_expected[2], 5)
    assert test30.num_beats == pytest.approx(test30_expected[3], 3)
    assert test30.beats == pytest.approx(test30_expected[4], 0.5)

    test31_expected = [75, [-0.2, 0.7], 15, 10, [0.75, 1.5, 2.25, 3.0, 3.75,
                       4.5, 5.25, 6.0, 6.75, 7.5, 8.25, 9.0, 9.75, 10.5,
                       11.25, 12.0, 12.75, 13.5, 14.25]]

    test31 = ecg_analyzer('test_data31.csv', 5)
    assert test31.mean_hr_bpm == pytest.approx(test31_expected[0], 5)
    assert test31.voltage_extremes == pytest.approx(test31_expected[1], 0.25)
    assert test31.duration == pytest.approx(test31_expected[2], 5)
    assert test31.num_beats == pytest.approx(test31_expected[3], 3)
    assert test31.beats == pytest.approx(test31_expected[4], 0.5)

    test32_expected = [75, [-350, 600], 15, 10, [0.75, 1.5, 2.25, 3.0, 3.75,
                       4.5, 5.25, 6.0, 6.75, 7.5, 8.25, 9.0, 9.75, 10.5,
                       11.25, 12.0, 12.75, 13.5, 14.25]]

    test32 = ecg_analyzer('test_data32.csv', 5)
    assert test32.mean_hr_bpm == pytest.approx(test32_expected[0], 5)
    assert test32.voltage_extremes == pytest.approx(test32_expected[1], 50)
    assert test32.duration == pytest.approx(test32_expected[2], 5)
    assert test32.num_beats == pytest.approx(test32_expected[3], 3)
    assert test32.beats == pytest.approx(test32_expected[4], 0.5)

def test_ecg_analyzer_raise():
    """
    Tests to see if the correct errors are raised
    """

    from data_analyzer import ecg_analyzer

    with pytest.raises(ValueError):
        ecg_analyzer('test_data1.csv', -2)

    with pytest.raises(TypeError):
        ecg_analyzer(2, 5)
