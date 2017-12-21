 

from dialog import Dialog
import csv
import time
import compute


def test_procedure(TESTNAME,testDict,ht):
    ####### CONFIG
    measures_to_take = 100
    d = Dialog(dialog="dialog")
    d.set_background_title("Testing: " + TESTNAME)
    d.msgbox("Disconnetti la schedina che fa click-click-click")


    # Start Measuring
    #ht.enable()
    time.sleep(1)
    ht.set_channel_gain(3, 5)

    d.gauge_start("Acquiring DAC Voltage VS Current measures")

    measures = {}
    raw_current_codes = range (int(4095/2-measures_to_take), int(4095/2+measures_to_take))
    # count from 0 to the total number of steps
    for i in range(len(raw_current_codes)):

        ht.set_current_raw(raw_current_codes[i])
        #pop all old measures
        while(ht.pop_measure() != None ):
            pass
        time.sleep(0.150)
        measures[i] = ht.pop_measure()
        d.gauge_update(int(float(i) / float(len(raw_current_codes)) * 100.0))
        if measures[i] is not None:
            measures[i]["raw_current_code"] = raw_current_codes[i]

    d.gauge_stop()

    
    
    testResult = compute.compute(testDict["asset_path"],measures,'raw_current_code','ch3')
    if(not testResult):
        return False
    if(not (0.0009-(0.0009*0.2)<=testResult['coeff']['slope']<=0.0009+(0.0009*0.2))):
        return False
    #ht.disable()
    return testResult
