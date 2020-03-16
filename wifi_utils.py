import os
import subprocess
import time
import atexit
from model import *

DN = open(os.devnull, 'w')
network = Network("", "", [])

#This will be used later when adding support for multiple cards.
def get_interfaces():
    interfaces = []
    try:
        iwcofig_cmd = subprocess.Popen(
            ["iwconfig"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except OSError:
        raise OSError("could not execute iwconfig. exiting ...")
    for line in iwcofig_cmd.communicate()[0].decode().split("\n"):
        if "IEEE 802.11" in line:
            interfaces.append(line[:line.find("  ")])
    network.set_interface_name(interfaces[0])
    return interfaces


def monitor_mode():
    try:
        subprocess.run(["ifconfig", network.interface_name, "down"], check=True)
        subprocess.run(["iwconfig", network.interface_name, "mode", "monitor"], check=True)
        subprocess.run(["ifconfig", network.interface_name, "up"], check=True)
    except:
        raise Exception("Cannot set interface to monitor mode.")
    output = subprocess.check_output(('grep', 'Mode'), stdin=subprocess.Popen(
        ('iwconfig', network.interface_name), stdout=subprocess.PIPE).stdout)
    if "Monitor" in output.decode():
        print(network.interface_name + " in monitor mode.")


def managed_mode():
    try:
        subprocess.run(["ifconfig", network.interface_name, "down"], check=True)
        subprocess.run(["iwconfig", network.interface_name, "mode", "managed"], check=True)
        subprocess.run(["ifconfig", network.interface_name, "up"], check=True)
    except:
        raise Exception("Cannot set interface to managed mode.")
    output = subprocess.check_output(('grep', 'Mode'), stdin=subprocess.Popen(
        ('iwconfig', network.interface_name), stdout=subprocess.PIPE).stdout)
    if "Managed" in output.decode():
        print(network.interface_name + " in managed mode.")


def set_channel(AP):
    try:
        print("Setting %s to channel %d" % (network.interface_name, AP.channel))
        subprocess.run(["iwconfig", network.interface_name,
                        "channel", str(AP.channel)], check=True)
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError(
            "Error setting %s to channel %d", network.interface_name, AP.channel)

def stop():
    print("exiting")
