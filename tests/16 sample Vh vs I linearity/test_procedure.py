from data_chan.instruments.fermiumlabs_labtrek_jv import hall_effect_apparatus as ht
import data_chan
from dialog import Dialog
import csv
import time
import compute

def operator_query_instructions():
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

    if not operator_query_instructions():
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
    print("cc")
    ht.set_channel_gain(scan, 3, 5)
    print("dd")
    d.gauge_start("Acquiring DAC Voltage VS Hall Vr measures")


    measures = {}
    raw_current_codes = range (int(4095/2-200), int(4095/2+200))

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

    destination_path = os.path.join(os.path.dirname(
        tests[TESTNAME]["path"]) , "assets/")

    # # Create assets directory if not existing
    # if not os.path.exists(destination_path):
    #     os.makedirs(destination_path)
    #
    # # Write output file
    # outfile = open(os.path.join(destination_path, "output.csv"), "w")
    # fieldnames = ["raw_current_code", "ch1", "ch2", "ch3", "ch5", "ch6", "ch7"]
    # csvwriter = csv.DictWriter(outfile, fieldnames=fieldnames,extrasaction='ignore')
    # csvwriter.writeheader()
    # for measure in measures:
    #     if measures[measure] is not None:
    #         csvwriter.writerow(measures[measure])
    test_result=compute.compute(tests[TESTNAME]["asset_path"],measures,'raw_current_code','ch3')
    ht.disconnect_device(scan)
    if test_result['status']:
        tests[TESTNAME]['data']['raw_data']=test_result['raw_data']
        tests[TESTNAME]['data']['coeff']=test_result['coeff']
        return True
    else:
        return False
