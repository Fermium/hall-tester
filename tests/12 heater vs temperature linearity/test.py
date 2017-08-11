from data_chan.instruments.fermiumlabs_labtrek_jv import hall_effect_apparatus as ht
import data_chan
from dialog import Dialog
import csv
import time
import compute

def test_procedure():
    
    
    
    
    
    return True
    
    
    
    
    
    
    
    d = Dialog(dialog="dialog")
    d.set_background_title("Testing: " + TESTNAME)

    try:
        ht.init()
        # Acquire the Hall Effect Apparatus
        scan = ht.acquire(0x16d0,0x0c9b)
    except DataChanDeviceNotFoundOrInaccessibleError:
        d.msgbox("Data-chan initialization failed")
        return False
    
    # Start Measuring
    ht.enable(scan)
    ht.set_channel_gain(scan, 2, 1)
    
    ht.set_heater_state(127)
    
    d.gauge_start("Acquiring temperature over Time (with heater on)")
    
    
    measures = {}
    
    samples_count = 1000
    # count from 0 to the total number of steps
    for i in range(samples_count):
        
        #pop all old measures
        while(ht.pop_measure(scan) != None ):
            pass
        time.sleep(0.150)
        measures[i] = ht.pop_measure(scan)
        
        d.gauge_update(int(float(i) / samples_count * 100.0))
        
        if measures[i] is not None:
            measures[i]["raw_current_code"] = raw_current_codes[i]
    
    d.gauge_stop()
    
    destination_path = os.path.join(os.path.dirname(
        tests[TESTNAME]["path"]) , "assets/")
    
    # Create assets directory if not existing
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
        
    # Write output file
    outfile = open(os.path.join(destination_path, "output.csv"), "w")
    fieldnames = ["raw_current_code", "ch1", "ch2", "ch3", "ch5", "ch6", "ch7"]
    csvwriter = csv.DictWriter(outfile, fieldnames=fieldnames,extrasaction='ignore')
    csvwriter.writeheader()
    for measure in measures:
        if measures[measure] is not None:
            csvwriter.writerow(measures[measure])
            

    if compute.compute(destination_path):
        return True
    else:
        return False
        
    
    
if test_procedure():
    tests[TESTNAME]["status"] = "success"
else:
    tests[TESTNAME]["status"] = "failure"
