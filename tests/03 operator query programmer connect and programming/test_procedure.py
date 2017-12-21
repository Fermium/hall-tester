import os
import boto3
import botocore
from dialog import Dialog
import subprocess

# Where to dowload the firmware from (amazon s3)
firmware_bucket_name = 'fermiumlabs-firmware-builds'
firmware_branch = "master"
firmware_commit_hash = "6e0de71ff0fbd3a51eee6cc2bc0a7685463a35d3"
firmware_filename = "main.hex"
firmware_path = "hall-firmware-v2/" + \
    firmware_branch + "/" + firmware_commit_hash + "/"

avrdude_mcu = "atmega32u4"
avrdude_programmer = "usbasp"
avrdude_fuses_flags = "-U lfuse:w:0x9e:m -U hfuse:w:0x99:m -U efuse:w:0xc3:m"


firmware_md5_filename = "checksums.md5"


def test_procedure(TESTNAME,testDict,ht):

    d = Dialog(dialog="dialog")
    d.set_background_title("Testing: " + TESTNAME)

    # Initialize s3
    s3 = boto3.resource('s3')



    # Attempt to download file
    try:
        with open(os.path.join(testDict["asset_path"], firmware_filename), 'wb') as data:
            s3.Bucket(firmware_bucket_name).download_fileobj(
                os.path.join(firmware_path, firmware_filename), data)
        with open(os.path.join(testDict["asset_path"], firmware_md5_filename), 'wb') as data:
            s3.Bucket(firmware_bucket_name).download_fileobj(
                os.path.join(firmware_path, firmware_md5_filename), data)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            d.msgbox("unable to download the firmware: 404 not found")
            return False
        else:
            print(e.response['Error']['Code'])
            d.msgbox("Exception raised while trying to download the firmware")
            return False
            raise

    # check md5 checksum
    md5sumreturncode = subprocess.call(
        "md5sum -c --ignore-missing --status checksums.md5", shell=True, cwd=testDict["asset_path"])
    if md5sumreturncode is 0:
        d.msgbox("Downloaded firmware from:\n\n- s3 bucket: " + firmware_bucket_name + "\n- branch: " + firmware_branch +
                 "\n- commit hash: " + firmware_commit_hash + "\n\nMD5 hash checked and resulted correct", width=60, height=15)
    else:
        d.msgbox("Downloaded a corrupt file, test failed!")
        return False

    d.msgbox(
        "Please connect the USBASP programmer to both board and PC, then press ok")


    # program the device
    with open(os.path.join(testDict["asset_path"], "avrdude.log"), 'w') as logfile:
        avrdudereturncode = subprocess.call("avrdude -p " + avrdude_mcu + " -c " + avrdude_programmer + " -U flash:w:" +
                                            firmware_filename + " " + avrdude_fuses_flags, shell=True, cwd=testDict["asset_path"], stdout=logfile, stderr=logfile)
        d.programbox(file_path=logfile.name, text="Avrdude programming:")
        if avrdudereturncode is not 0:
            d.msgbox("Programming failed, test failed!")
            return False
    d.msgbox(
        "Please disconnect the USBASP programmer")
    return True
