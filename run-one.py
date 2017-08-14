import glob
import sys
import os
from dialog import Dialog as Masterdialog
import time
import signal

masterdialog = Masterdialog(dialog="dialog")
masterdialog.set_background_title(
    "Fermium LABS testing procedure - Hall Effect apparatus")

testtorun = masterdialog.inputbox("Which test do you want to run? ")


if testtorun[0] == "ok": #user inserted a number and did not press cancel
    try:
        
        int(testtorun[1])
    except ValueError:
        print("Please insert an integer number")
        sys.exit(1)
else: #user pressed cancel
    sys.exit(0)


testspaths = glob.glob("./tests/" + testtorun[1] + "*/test.py")
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

exitstatus = 0

# Execute tests
for TESTNAME in tests:
    # cleanup files
    files = glob.glob(os.path.join(os.path.dirname(
        tests[TESTNAME]["path"]) + "/" + "assets/*"))
    for f in files:
        os.remove(f)
            
    # clear screen
    print(chr(27) + "[2J")
    
    # Execute test
    testfile = open(tests[TESTNAME]["path"], "r")
    sys.path.append(os.path.dirname(tests[TESTNAME]["path"]))
    exec(testfile.read())
    sys.path.remove(os.path.dirname(tests[TESTNAME]["path"]))
    
    masterdialog.msgbox("Test" + " \"" + TESTNAME + "\" " + "exit status is " + tests[TESTNAME]["status"], width=60)
    
    # Exit with 1 if at least one test fails
    if tests[TESTNAME]["status"] is not "success":
        exitstatus = 1


print(chr(27) + "[2J")
sys.exit(exitstatus)
