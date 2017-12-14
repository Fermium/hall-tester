#!/home/d/anaconda3/bin/python
import sys
import glob
import os
sys.path.insert(0, os.path.join('.','compute'))
from dialog import Dialog as Masterdialog
import signal
import json
from upload_to_s3 import upload_assets_s3
import argparse
from collections import OrderedDict
import importlib

parser = argparse.ArgumentParser("Run HW Tests")
parser.add_argument("--filter", dest="filters", type=str,
                    nargs="+", help="Filter the tests by name", default=False)
parser.add_argument("--quick", dest="quick",
                    action='store_true', help="Skip the dialogs and execute the script directly")
parser.add_argument("--s3", dest="s3",
                    action='store_true', help="upload on S3")
args = parser.parse_args()

# CONFIG
product_id = 'ltk-hall'
bucket_name = 'fermiumlabs-manufacturing-data'
assetglob = "assets/**/*"
title = "Fermium LABS testing procedure - Hall Effect apparatus"
####################################################

masterdialog = Masterdialog(dialog="dialog")
masterdialog.set_background_title(title)

testspaths = glob.glob("./tests/*/test_procedure.py")
testspaths.sort()
print([os.path.dirname(testpath).split("/").pop() for testpath in testspaths])
# Fundamental test dict
tests = OrderedDict()
print(tests)
for testpath in testspaths:
    name = os.path.dirname(testpath).split("/").pop()
    tests[name] = {}
    tests[name]["path"] = os.path.abspath(testpath)
    tests[name]["status"] = "not yet run"
    tests[name]["data"] = {}
    #tests[name]["asset_path"] = os.path.join(os.path.dirname(tests[name]["path"]), "assets/")
    tests[name]["asset_path"] = os.path.join(".", "assets", name)
    print(tests[name]["asset_path"])
del testspaths
for test in tests:
    #cleanup files
     for f in glob.glob(os.path.join(tests[test]["asset_path"], "*")):
         os.remove(f)
     # Create assets directory if not existing
     if not os.path.exists(tests[test]["asset_path"]):
         os.makedirs(tests[test]["asset_path"])

if args.filters:
    for filter in args.filters:
        tests = {k: v for (k, v) in tests.items() if filter in k}


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
    if not args.quick:
        show_master_dialog()
    testfile = open(tests[TESTNAME]["path"], "r")

    # while tests[TESTNAME]["status"] != "success":
    sys.path.append(os.path.dirname(tests[TESTNAME]["path"]))
    if 'test_procedure' in sys.modules:
        importlib.reload(test_procedure)
    else:
        import test_procedure
    tests[TESTNAME]['data']=test_procedure.test_procedure(TESTNAME,tests[TESTNAME])
    if tests[TESTNAME]['data']:
        tests[TESTNAME]["status"] = "success"
    else:
        tests[TESTNAME]["status"] = "failure"
    #exec(testfile.read())
    sys.path.remove(os.path.dirname(tests[TESTNAME]["path"]))

    with open(os.path.join(tests[TESTNAME]["asset_path"], "dump.json"), "w") as fp:
        json.dump(tests[TESTNAME], fp, sort_keys=True, indent=4)

if not args.quick:
    show_master_dialog()


if args.s3:
    masterdialog.msgbox("Uploading result on S3")
    upload_assets_s3(assetglob, product_id, bucket_name)


print(chr(27) + "[2J")
#time.sleep(2)
#sys.exit(0)
