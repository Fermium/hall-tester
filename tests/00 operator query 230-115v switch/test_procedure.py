import sys
import os
from dialog import Dialog


def test_procedure(TESTNAME,testDict,ht):
    d = Dialog(dialog="dialog", autowidgetsize=True)

    d.set_background_title("Testing: " + TESTNAME)
    while True:
        linevoltage = list(d.inputbox(
            "Quale e' la tensione indicata sullo switch vicino al trasformatore?"))

        # remove the volts symbol
        linevoltage[1] = linevoltage[1].replace("v", "").replace("V", "")

        # The user pressed cancel
        if linevoltage[0] is not "ok":
            d.msgbox("Test Interrotto")
            return False

        # test if it is a number
        try:
            int(linevoltage[1])
            if int(linevoltage[1]) is not 230:
                d.msgbox("Test Fallito! Lo switch deve essere impostato a 230v")
                return False
            else:
                d.msgbox("Test Superato")
                return True
        except ValueError:
            d.msgbox("Inserisci un numero!")
            return False
