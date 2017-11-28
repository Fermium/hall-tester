from data_chan.instruments.fermiumlabs_labtrek_jv import hall_effect_apparatus as ht
import data_chan
from dialog import Dialog
import csv
import time
import compute

####### CONFIG
measures_to_take = 100

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
    print(1)
    ht.enable(scan)
    print(2)
    ht.set_channel_gain(scan, 3, 5)
    print(3)
    
    d.gauge_start("Acquiring DAC Voltage VS Current measures")
    
    print(4)
    measures = {}
    raw_current_codes = range (int(4095/2-measures_to_take), int(4095/2+measures_to_take)) 
    print(5)
    # count from 0 to the total number of steps
    for i in range(len(raw_current_codes)):
        
        print("a")
        ht.set_current_raw(scan,raw_current_codes[i])
        #pop all old measures
        print("b")
        while(ht.pop_measure(scan) != None ):
            pass
        print("c")
        time.sleep(0.150)
        print("d")
        measures[i] = ht.pop_measure(scan)
        print("e")
        d.gauge_update(int(float(i) / float(len(raw_current_codes)) * 100.0))
        print("f")
        if measures[i] is not None:
            measures[i]["raw_current_code"] = raw_current_codes[i]
        print("g")
    
    d.gauge_stop()
    
    # Create assets directory if not existing
    if not os.path.exists(tests[TESTNAME]["asset_path"]):
        os.makedirs(tests[TESTNAME]["asset_path"])
    # Write output file
    outfile = open(os.path.join(tests[TESTNAME]["asset_path"], "output.csv"), "w")
    fieldnames = ["raw_current_code", "ch1", "ch2", "ch3", "ch5", "ch6", "ch7"]
    csvwriter = csv.DictWriter(outfile, fieldnames=fieldnames, 
                        extrasaction='ignore')
    csvwriter.writeheader()
    for measure in measures:
        if measures[measure] is not None:
            csvwriter.writerow(measures[measure])

    if compute.compute(tests[TESTNAME]["asset_path"]):
        return True
    else:
        return False
        
    
    
if test_procedure():
    tests[TESTNAME]["status"] = "success"
else:
    tests[TESTNAME]["status"] = "failure"
