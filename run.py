import glob
import sys
import os
from dialog import Dialog as Masterdialog
import time
import signal


testspaths = glob.glob("./tests/*/test.py")
testspaths.sort()

# Fundamental test dict
tests = {}
for testpath in testspaths:
    tests[os.path.dirname(testpath).split("/").pop()] = {}
    tests[os.path.dirname(testpath).split("/").pop()]["path"] = testpath
    tests[os.path.dirname(testpath).split("/").pop()]["status"] = "not yet run"
del testspaths


def show_master_dialog():
    """show quick summary of the progress"""
    def calculate_progress_percentage(d):
        """Calculates progress of the testing operation"""
        successcounter = 0
        for test in d:
            if d[test]["status"] is "success":
                successcounter += 1
        totalcounter = 0
        for test in d:
            totalcounter += 1
        return int(successcounter / totalcounter * 100)
    masterdialog = Masterdialog(dialog="dialog")
    masterdialog.set_background_title(
        "Fermium LABS testing procedure - Hall Effect apparatus")
    percent = calculate_progress_percentage(tests)
    masterdialog.mixedgauge("TEST SUMMARY - Press ENTER key to continue...",
                            percent=percent, elements=[(k, v["status"]) for k, v in tests.items()])
    input()


def signal_handler(signal, frame):
    """Manage attemps to shut down the program"""
    print(chr(27) + "[2J")
    sys.exit(0)

        


signal.signal(signal.SIGINT, signal_handler)


# Execute tests
for TESTNAME in tests:
    print(chr(27) + "[2J")
    show_master_dialog()
    testfile = open(tests[TESTNAME]["path"], "r")
    #while tests[TESTNAME]["status"] != "success":
    exec(testfile.read())


show_master_dialog()


print(chr(27) + "[2J")
sys.exit(0)
        
        
        
        
