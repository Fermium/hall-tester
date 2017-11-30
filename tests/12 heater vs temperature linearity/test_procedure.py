from data_chan.instruments.fermiumlabs_labtrek_jv import hall_effect_apparatus as ht
import data_chan
from dialog import Dialog
import csv
import time
import compute
import pdb
############## CONFIG
sleep = 0.5
samples_count = 1000


def test_procedure(TESTNAME,testDict):

    d = Dialog(dialog="dialog")
    d.set_background_title("Testing: " + TESTNAME)

    d.msgbox("Connect the heater and press OK")

    try:
        ht.init()
        # Acquire the Hall Effect Apparatus
        scan = ht.acquire(0x16d0, 0x0c9b)
    except DataChanDeviceNotFoundOrInaccessibleError:
        d.msgbox("Data-chan initialization failed")
        return False

    # Start Measuring
    ht.enable(scan)
    ht.set_channel_gain(scan, 2, 1)
    ht.set_current_fixed(scan, 0.05)

    ht.set_heater_state(scan, 127)

    d.gauge_start("Acquiring temperature over Time (with heater on)")

    measures = {}
    # count from 0 to the total number of steps
    for i in range(samples_count):
        time.sleep(sleep)

        # pop all old measures
        while(ht.pop_measure(scan) != None):
            pass
        measures[i] = ht.pop_measure(scan)
        if measures[i] is not None:
            measures[i]["i"] = i * sleep

        d.gauge_update(int(float(i) / samples_count * 100.0))



    d.gauge_stop()

    ht.disconnect_device(scan)
    return compute.compute(testDict["asset_path"],measures,'raw_current_code','ch3')
