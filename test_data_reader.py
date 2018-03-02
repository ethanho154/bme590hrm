import pytest

def test_ecg_reader():
    from data_reader import ecg_reader

    with pytest.raises(TypeError):
        ecg_reader(2, 5)
