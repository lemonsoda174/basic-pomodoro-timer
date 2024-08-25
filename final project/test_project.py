from project import mode_check, time_check, timer
import pytest
def test_mode_check():
    assert mode_check("TiMeR") == "Timer"
    assert mode_check("sToPwaTcH") == "Stopwatch"
    with pytest.raises(SystemExit):
        mode_check("random input")
def test_time_check():
    assert time_check("01:02:03") == [1, 2, 3]
    assert time_check("99:59:59") == [99, 59, 59]
    with pytest.raises(SystemExit):
        time_check("00:60:60")
        time_check("100:00:00")
def test_timer():
    assert timer("Timer", [0, 0, 5]) == True
    with pytest.raises(SystemExit):
        timer("not ok", [0, 0, 5])
    """this function only prints out as a sort of display and returns nothing useful"""
        