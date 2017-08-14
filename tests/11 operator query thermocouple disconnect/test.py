from data_chan.instruments.fermiumlabs_labtrek_jv import hall_effect_apparatus as ht
import data_chan
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from dialog import Dialog


def test_procedure():   
    
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
    
    
    d.msgbox("Connect the thermocouple and press ok")
    #pop all old measures
    while(ht.pop_measure(scan) != None ):
        pass
    
    # take an average of the thermocouple voltage
    average = 0
    for i in range(10):
        time.sleep(0.2)
        popped_meas = ht.pop_measure(scan)
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
    while(ht.pop_measure(scan) != None ):
        pass
    
    # take an average of the thermocouple voltage
    average = 0
    for i in range(10):
        time.sleep(0.2)
        popped_meas = ht.pop_measure(scan)
        if popped_meas is not None:
            average += popped_meas["ch2"]
    average = average / 10
    if average >= 2.0:
        pass
    else:
        d.msgbox("termocouple pullup not triggered, measured an avg of " + str(average) + " V")
        return False
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
        popped_meas = ht.pop_measure(scan)
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
    
    
    
if test_procedure():
    tests[TESTNAME]["status"] = "success"
else:
    tests[TESTNAME]["status"] = "failure"
