import glob
import sys
import os
from dialog import Dialog as Masterdialog
import signal
import json

masterdialog = Masterdialog(dialog="dialog")
masterdialog.set_background_title(
    "Fermium LABS testing procedure - Hall Effect apparatus")

testspaths = glob.glob("./tests/*/test.py")
print(testspaths)
testspaths.sort()

# Fundamental test dict
tests = {}
for testpath in testspaths:
    name = os.path.dirname(testpath).split("/").pop()
    tests[name] = {}
    tests[name]["path"] = os.path.abspath(testpath)
    tests[name]["status"] = "not yet run"
    tests[name]["data"] = {}
    #tests[name]["asset_path"] = os.path.join(os.path.dirname(tests[name]["path"]), "assets/")
    tests[name]["asset_path"] = os.path.join(".", "assets" """<--- put here the serial of the piece""", name)
    print(tests[name]["asset_path"])
del testspaths


for test in tests:
        # cleanup files
        for f in glob.glob(os.path.join(tests[test]["asset_path"] , "*")):
            os.remove(f)
        # Create assets directory if not existing
        if not os.path.exists(tests[test]["asset_path"]):
            os.makedirs(tests[test]["asset_path"])

def show_master_dialog():
    """show quick summary of the progress"""
    def calculate_progress_percentage(d):
        """Calculates progress of the testing operation"""
        successcounter = 0
        for test in d:
            if d[test]["status"] != "not yet run":
                successcounter += 1
        totalcounter = 0
        for test in d:
            totalcounter += 1
        return int(successcounter / totalcounter * 100)

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

    # clear screen
    print(chr(27) + "[2J")
    show_master_dialog()
    testfile = open(tests[TESTNAME]["path"], "r")
    # while tests[TESTNAME]["status"] != "success":
    sys.path.append(os.path.dirname(tests[TESTNAME]["path"]))
    #temporary solution
    if(not any(num in TESTNAME[:2] for num in ("9","8","11","13","14","15","17"))):
        exec(testfile.read())
    sys.path.remove(os.path.dirname(tests[TESTNAME]["path"]))
    with open(os.path.join(tests[TESTNAME]["asset_path"], "dump.json"), "w") as fp:
        json.dump(tests[TESTNAME], fp, sort_keys=True, indent=4)

show_master_dialog()


print(chr(27) + "[2J")
sys.exit(0)
