import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from dialog import Dialog
import time


def test_procedure(TESTNAME,testDict,ht):
    

    

    d = Dialog(dialog="dialog")
    d.set_background_title("Testing: " + TESTNAME)





    # Start Measuring
    #ht.enable()
    time.sleep(1)
    ht.set_channel_gain(2, 5)


    d.msgbox("Connect the thermocouple and press ok")
    #pop all old measures
    while(ht.pop_measure() != None ):
        pass

    # take an average of the thermocouple voltage
    average = 0
    for i in range(10):
        time.sleep(0.2)
        popped_meas = ht.pop_measure()
        if popped_meas is not None:
            average += popped_meas["ch2"]
    average = average / 10
    if average <= 2.0:
        pass
    else:
        d.msgbox("termocouple not connected, measured an avg of " + str(average) + " V")
        return False


    d.msgbox("Disconnect the thermocouple and press ok")
    #pop all old measures
    while(ht.pop_measure() != None ):
        pass

    # take an average of the thermocouple voltage
    average = 0
    for i in range(10):
        time.sleep(0.2)
        popped_meas = ht.pop_measure()
        if popped_meas is not None:
            average += popped_meas["ch2"]
    average = average / 10


    
    


    if average >= 2.0:
        pass
    else:
        d.msgbox("termocouple pullup not triggered, measured an avg of " + str(average) + " V")
        return False
    #ht.disable()
    return True
"""
    win = pg.GraphicsWindow()
    win.setWindowTitle(TESTNAME)

    meas = {"ch2":{}}
    meas["ch2"]["name"] = "Thermocouple voltage"

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
    if __name__ == '__main__':
        import sys
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
"""
