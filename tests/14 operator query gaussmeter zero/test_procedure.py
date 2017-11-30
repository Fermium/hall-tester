from data_chan.instruments.fermiumlabs_labtrek_jv import hall_effect_apparatus as ht
import data_chan
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from dialog import Dialog


def test_procedure(TESTNAME,testDict):

    d = Dialog(dialog="dialog")
    d.set_background_title("Testing: " + TESTNAME)

    try:
        ht.init()
        # Acquire the Hall Effect Apparatus
        scan = ht.acquire(0x16d0,0x0c9b)
    except Exception:
        d.msgbox("Data-chan initialization failed")
        return False



    # Start Measuring
    ht.enable(scan)
    ht.set_channel_gain(scan, 2, 5)


    d.msgbox("Move the gaussmeter probe well away from any magnetic field")
    #pop all old measures
    while(ht.pop_measure(scan) != None ):
        pass

    # The abs value of voltage to test for
    simmetry_margin = 0.01

    # take an average of the thermocouple voltage
    average = 0
    for i in range(50):
        time.sleep(0.2)
        popped_meas = ht.pop_measure(scan)
        if popped_meas is not None:
            average += popped_meas["ch2"]
    average = average / 50
    ht.disconnect_device(scan)
    if average <= simmetry_margin and average >= -simmetry_margin:
        return True
    else:
        return False
