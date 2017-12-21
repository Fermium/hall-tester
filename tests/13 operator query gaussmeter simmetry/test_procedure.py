import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from dialog import Dialog


def operator_query_instructions(TESTNAME):
    d = Dialog(dialog="dialog")

    d.set_background_title("Testing: " + TESTNAME)

    testquery = d.msgbox("Check that inverting the gaussmeter you get the same abs value of voltage", width=60)

    # The user pressed cancel
    if testquery is not "ok":
        d.msgbox("Test Interrotto")
        return False
    else: #the user pressed ok
        return True


def operator_query_passfail(TESTNAME):
    d = Dialog(dialog="dialog")

    d.set_background_title("Testing: " + TESTNAME)

    testquery = d.yesno("Was the voltage inverting the probe the same?", width=60, yes_label="Yes, it was", no_label="No, It wasn't")

    # The user pressed cancel
    if testquery is not "ok":
        d.msgbox("Test Fallito.")
        return False
    else: #the user pressed ok
        return True




def test_procedure(TESTNAME,testDict,ht):
    

    
    
    
    d = Dialog(dialog="dialog")

    d.set_background_title("Testing: " + TESTNAME)

    if not operator_query_instructions(TESTNAME):
        return False



    # Start Measuring
    #ht.enable()
    time.sleep(1)
    ht.set_channel_gain(5, 5)

    # Set CC gen
    ht.set_current_fixed( 0.3)

    win = pg.GraphicsWindow()
    win.setWindowTitle(TESTNAME)
    meas = {"ch7":{}}
    meas["ch7"]["name"] = "Hall voltage (unamplified)"
    for key in meas:
        meas[key]["plotobj"] = win.addPlot(title=meas[key]["name"])
        meas[key]["data"] = [0]*100
        meas[key]["curveobj"] = meas[key]["plotobj"].plot(meas[key]["data"])

    def update():
        popped_meas = ht.pop_measure()
        if popped_meas is not None:
            for key in meas:
                meas[key]["data"][:-1] = meas[key]["data"][1:]
                meas[key]["data"][-1] = popped_meas[key]
                meas[key]["curveobj"].setData(meas[key]["data"])

    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(50)

    ## Start Qt event loop unless running in interactive mode or using pyside.
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
    
    #ht.disable()
    return operator_query_passfail(TESTNAME)
