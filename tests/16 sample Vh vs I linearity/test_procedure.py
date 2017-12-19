from data_chan.instruments.fermiumlabs_labtrek_jv import hall_effect_apparatus as ht
import data_chan
from dialog import Dialog
import csv
import time
import compute

def operator_query_instructions(TESTNAME):
    d = Dialog(dialog="dialog")

    d.set_background_title("Testing: " + TESTNAME)

    testquery = d.msgbox("Please put the sample into the magnetic field in a stable position", width=60)

    # The user pressed cancel
    if testquery is not "ok":
        d.msgbox("Test Interrotto")
        return False
    else: #the user pressed ok
        return True


def test_procedure(TESTNAME,testDict):
    d = Dialog(dialog="dialog")
    d.set_background_title("Testing: " + TESTNAME)

    if not operator_query_instructions(TESTNAME):
        return False


    try:
        ht.init()
        # Acquire the Hall Effect Apparatus
        scan = ht.acquire(0x16d0,0x0c9b)
    except Exception:
        d.msgbox("Data-chan initialization failed")
        return False

    # Start Measuring
    ht.enable(scan)
    ht.set_channel_gain(scan, 3, 5)
    d.gauge_start("Acquiring DAC Voltage VS Hall Vr measures")


    measures = {}
    raw_current_codes = range (int(2000), int(2100))

    # count from 0 to the total number of steps
    for i in range(len(raw_current_codes)):

        ht.set_current_raw(scan,raw_current_codes[i])
        #pop all old measures
        while(ht.pop_measure(scan) != None ):
            pass
        time.sleep(0.150)
        measures[i] = ht.pop_measure(scan)

        d.gauge_update(int(float(i) / float(len(raw_current_codes)) * 100.0))

        if measures[i] is not None:
            measures[i]["raw_current_code"] = raw_current_codes[i]

    d.gauge_stop()

    ht.disconnect_device(scan)
    ht.deinit()
    testResult = compute.compute(testDict["asset_path"],measures,'raw_current_code','ch6')
    if(not testResult):
        return False
    if(not (-0.0014-(-0.0014*0.2)<=testResult['coeff']['slope']<=-0.0014+(-0.0014*0.2))):
        return False
    return testResult
