import sys
import os
from dialog import Dialog


def test_procedure(TESTNAME,testDict):

    d = Dialog(dialog="dialog")

    d.set_background_title("Testing: " + TESTNAME)

    testquery = d.msgbox("Scollega la HUB board di test e collega la HUB board definitiva", width=60)

    # The user pressed cancel
    if testquery is not "ok":
        d.msgbox("Test Interrotto")
        return False
    else: #the user pressed ok
        return True

    # this line should never be executed
    return False
