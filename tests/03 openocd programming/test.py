import sys, os
import boto3
import botocore
from dialog import Dialog
from pathlib import Path
import subprocess

# Where to dowload the firmware from (amazon s3)
firmware_bucket_name = 'fermiumlabs-firmware-builds'
firmware_branch = "develop"
firmware_commit_hash = "d5826a9fbcaca5789f16ed46055cb2280b515cf4"
firmware_filename = "main.hex"
firmware_path = "hall-firmware-v2/develop/d5826a9fbcaca5789f16ed46055cb2280b515cf4/"

destination_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/")
firmware_md5_filename = "checksums.md5"

def test_procedure():
    
    d = Dialog(dialog="dialog")
    d.set_background_title("Testing: " + TESTNAME)

    # Initialize s3
    s3 = boto3.resource('s3')
    
    # Create assets directory if not existing
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    # Attempt to download file
    try:
        with open(os.path.join(destination_path + firmware_filename), 'wb') as data:
            s3.Bucket(firmware_bucket_name).download_fileobj(os.path.join(firmware_path + firmware_filename), data)
        with open(os.path.join(destination_path + firmware_md5_filename), 'wb') as data:
            s3.Bucket(firmware_bucket_name).download_fileobj(os.path.join(firmware_path + firmware_md5_filename), data)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            d.msgbox("unable to download the firmware: 404 not found")
            return False
        else:
            d.msgbox("Exception raised while trying to download the firmware")
            return False
            raise


    # check md5 checksum
    md5sumreturncode = subprocess.call("md5sum -c --ignore-missing --status checksums.md5", shell=True, cwd=destination_path)
    if md5sumreturncode is 0:
        d.msgbox("Downloaded firmware from:\n\n- s3 bucket: " + firmware_bucket_name + "\n- branch: " + firmware_branch + "\n- commit hash: " + firmware_commit_hash + "\n\nMD5 hash checked and resulted correct",width=60, height=15)
    else:
        d.msgbox("Downloaded a corrupt file, test failed!")
        return False



"""
if test_procedure():
    tests[TESTNAME]["status"] = "success"
else:
    tests[TESTNAME]["status"] = "failure"
"""
