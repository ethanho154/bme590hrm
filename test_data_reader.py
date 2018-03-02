import pytest

def test_ecg_reader():
    """
    Test to see if data is read properly
    """

    from data_reader import ecg_reader

    d = ecg_reader("small_test.csv")
    time = [19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
            19, 19, 19, 19, 19, 19, 19, 19, 19, 19]
    voltage = [46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46,
               46, 46, 46, 46, 46, 46, 46, 46, 46, 46]
    assert d.time == time
    assert d.voltage == voltage

def test_ecg_reader_exc():
    """
    Test to see if correct exceptions are raised
    """

    from data_reader import ecg_reader

    with pytest.raises(TypeError):
        ecg_reader(2)

    with pytest.raises(TypeError):
        ecg_reader([])
