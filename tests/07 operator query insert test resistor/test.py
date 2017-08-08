import sys
import os
from dialog import Dialog


def test_procedure():

    d = Dialog(dialog="dialog")

    d.set_background_title("Testing: " + TESTNAME)

    testquery = d.msgbox("Collega la scheda di test con resistore da 4ohm allo strumento attraverso il cavo DB25", width=60)

    # The user pressed cancel
    if testquery is not "ok":
        d.msgbox("Test Interrotto")
        return False
    else: #the user pressed ok
        return True

    # this line should never be executed
    return False


if test_procedure():
    tests[TESTNAME]["status"] = "success"
else:
    tests[TESTNAME]["status"] = "failure"
