import glob
import sys
import os
from dialog import Dialog as Masterdialog
import time
import signal

masterdialog = Masterdialog(dialog="dialog")
masterdialog.set_background_title(
    "Fermium LABS testing procedure - Hall Effect apparatus")

testtorun = input("Which test do you want to run? ")
try:
    int(testtorun)
except ValueError:
    print("Please insert an integer number")
    sys.exit(0)


testspaths = glob.glob("./tests/" + testtorun + "*/test.py")
testspaths.sort()

# Fundamental test dict
tests = {}
for testpath in testspaths:
    tests[os.path.dirname(testpath).split("/").pop()] = {}
    tests[os.path.dirname(testpath).split("/").pop()
          ]["path"] = os.path.abspath(testpath)
    tests[os.path.dirname(testpath).split("/").pop()]["status"] = "not yet run"
del testspaths


if len(tests) == 0:
    print("No test found")
    sys.exit(0)


def signal_handler(signal, frame):
    """Manage attemps to shut down the program"""
    print(chr(27) + "[2J")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


# Execute tests
for TESTNAME in tests:
    # cleanup files
    files = glob.glob(os.path.join(os.path.dirname(
        tests[TESTNAME]["path"]) + "/" + "assets/*"))
    for f in files:
        os.remove(f)
            
    # clear screen
    print(chr(27) + "[2J")
    
    testfile = open(tests[TESTNAME]["path"], "r")
    # while tests[TESTNAME]["status"] != "success":
    exec(testfile.read())


print(chr(27) + "[2J")
sys.exit(0)
