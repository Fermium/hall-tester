from data_chan.instruments.fermiumlabs_labtrek_jv import hall_effect_apparatus as ht
import data_chan
from dialog import Dialog
import time

def test_procedure(TESTNAME,testDict):
    d = Dialog(dialog="dialog")
    d.set_background_title("Testing: " + TESTNAME)


    try:
        # Initialize
        ht.init()

        # Acquire the Hall Effect Apparatus
        scan = ht.acquire(0x16d0,0x0c9b)
        # Start Measuring
        ht.enable(scan)

        # Set CC gen
        ht.set_current_fixed(scan, 0.01)

        # Check that the reported measures are ok
        count_correct_meas = 0
        for i in range (1,25):
            meas = ht.pop_measure(scan)
            if meas is not None:
                count_correct_meas += 1
                d.infobox(str(meas).replace(", ", ",\n"), width=60, height=20)
            time.sleep(0.3)

        ht.disconnect_device(scan)

        if count_correct_meas < 20:
            d.msgbox("Too many measures were empty! fail", width=60)
            return False


    # Except problems in conneting to the device or retrieving measures
    except Exception as e:

        d.msgbox(str(e), width=60)
        import traceback

        tb = traceback.format_exc()
        d.scrollbox(str(tb))
        return False
        pass
    return True
