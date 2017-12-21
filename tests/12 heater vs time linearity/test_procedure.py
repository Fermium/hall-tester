from dialog import Dialog
import time
import compute
############## CONFIG
sleep = 0.5
samples_count = 1000


def test_procedure(TESTNAME,testDict,ht):
    print(ht)
    

    d = Dialog(dialog="dialog")
    d.set_background_title("Testing: " + TESTNAME)

    d.msgbox("Connect the heater and press OK")

    try:
        # Acquire the Hall Effect Apparatus
        scan = ht.acquire(0x16d0, 0x0c9b)
    except:
        d.msgbox("Data-chan initialization failed")
        return False
    
    time.sleep(1)
    # Start Measuring
    ht.enable()
    time.sleep(sleep)

    ht.set_heater_state(255)
    time.sleep(sleep)
    d.gauge_start("Acquiring temperature over Time (with heater on)")

    measures = {}
    # count from 0 to the total number of steps
    for i in range(samples_count):
        
        # pop all old measures
        while(ht.pop_measure() != None):
            pass
        time.sleep(sleep)
        measures[i] = ht.pop_measure()
        if measures[i] is not None:
            measures[i]["i"] = i * 2 * sleep

        d.gauge_update(int(float(i) / samples_count * 100.0))

    d.gauge_stop()
    ht.disconnect_device()
    
    testResult = compute.compute(testDict["asset_path"],measures,'i','ch2')
    if(not testResult):
        return False
    if(not (testResult['coeff']['slope']>=0.0005)):
        return False
    return testResult
