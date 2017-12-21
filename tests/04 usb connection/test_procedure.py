
from dialog import Dialog
import time

def test_procedure(TESTNAME,testDict,ht):
    
    
    
    d = Dialog(dialog="dialog")
    d.set_background_title("Testing: " + TESTNAME)


    try:
        # Initialize
        

        # Acquire the Hall Effect Apparatus
        ht.acquire(0x16d0,0x0c9b)

        # Start Measuring
        ht.enable()
        time.sleep(1)

        # Set CC gen
        ht.set_current_fixed( 0.01)

        # Check that the reported measures are ok
        count_correct_meas = 0
        for i in range (1,25):
            meas = ht.pop_measure()
            if meas is not None:
                count_correct_meas += 1
                d.infobox(str(meas).replace(", ", ",\n"), width=60, height=20)
            time.sleep(0.3)

        ht.disconnect_device()
        
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
