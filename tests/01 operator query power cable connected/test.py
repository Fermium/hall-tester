import sys, os

from dialog import Dialog
#get name from path
name = os.path.dirname(os.path.realpath(__file__)).split("/").pop()


d = Dialog(dialog="dialog")

d.set_background_title("Testing: " + name)

test = d.msgbox("Collega il cavo IEC di alimentazione", width=60)


# The user pressed cancel
if linevoltage[0] is not "ok":
    d.msgbox("Test Interrotto")
    sys.exit(1)
else:
    sys.exit(0)


# this line should never be executed
sys.exit(1)
