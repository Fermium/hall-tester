import sys, os

from dialog import Dialog
#get name from path
name = os.path.dirname(os.path.realpath(__file__)).split("/").pop()


d = Dialog(dialog="dialog", autowidgetsize=True)

d.set_background_title("Testing: " + name)

linevoltage = list(d.inputbox("Quale e' la tensione indicata sullo switch vicino al trasformatore?"))

# remove the volts symbol
linevoltage[1] = linevoltage[1].replace("v","").replace("V","")

# The user pressed cancel
if linevoltage[0] is not "ok":
    d.msgbox("Test Interrotto")
    sys.exit(1)

# test if it is a number
try:
    int(linevoltage[1])
except ValueError:
    d.msgbox("Inserisci un numero!")
    sys.exit(1)


if int(linevoltage[1]) is not 230 :
    d.msgbox("Test Fallito! Lo switch deve essere impostato a 230v")
    sys.exit(1)
else:
    d.msgbox("Test Superato")
    sys.exit(0)


# this line should never be executed
sys.exit(1)
