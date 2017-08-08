from data_chan.instruments.fermiumlabs_labtrek_jv import hall_effect_apparatus as ht

def test_procedure():
    try:
        ht.init()
        scan = ht.acquire(0x16d0,0x0c9b)
        ht.enable(scan)
        ht.set_current_fixed(scan, 0.01)
        for i in range (1,25):
            ht.pop_measure()
        ht.disconnect_devide()
    except:
        return False
        pass
    return True
    
    
if test_procedure():
    tests[TESTNAME]["status"] = "success"
else:
    tests[TESTNAME]["status"] = "failure"
