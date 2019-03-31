import os
import subprocess
import time
import atexit
from model import *

DN = open(os.devnull, 'w')
network = Network("", [])

#This will be used later when adding support for multiple cards.
def get_interfaces():
    interfaces = []
    try:
        iwcofig_cmd = subprocess.Popen(
            ["iwconfig"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except OSError:
        raise OSError("could not execute iwconfig. exiting ..")
    for line in iwcofig_cmd.communicate()[0].decode().split("\n"):
        if "IEEE 802.11" in line:
            interfaces.append(line[:line.find("  ")])
    return interfaces


def monitor_mode(iface):
    try:
        subprocess.run(["ifconfig", iface, "down"], check=True)
        subprocess.run(["iwconfig", iface, "mode", "monitor"], check=True)
        subprocess.run(["ifconfig", iface, "up"], check=True)
    except:
        raise Exception("Cannot set interface to monitor mode.")
    output = subprocess.check_output(('grep', 'Mode'), stdin=subprocess.Popen(
        ('iwconfig', iface), stdout=subprocess.PIPE).stdout)
    if "Monitor" in output.decode():
        print(iface + " in monitor mode.")


def managed_mode(iface):
    try:
        subprocess.run(["ifconfig", iface, "down"], check=True)
        subprocess.run(["iwconfig", iface, "mode", "managed"], check=True)
        subprocess.run(["ifconfig", iface, "up"], check=True)
    except:
        raise Exception("Cannot set interface to managed mode.")
    output = subprocess.check_output(('grep', 'Mode'), stdin=subprocess.Popen(
        ('iwconfig', iface), stdout=subprocess.PIPE).stdout)
    if "Managed" in output.decode():
        print(iface + " in managed mode.")


def run_NetworkManeger():
    try:
        subprocess.run(["service", "NetworkManager", "restart"], check=True)
    except:
        raise Exception("Cannot start NetworkManager service.")


def iwlist_scan(iface):
    network.set_interface(iface)
    count = 0
    output = subprocess.check_output(('grep', 'Mode'), stdin=subprocess.Popen(
        ('iwconfig', iface), stdout=subprocess.PIPE).stdout)
    if "Monitor" in output.decode():
        managed_mode(iface)
    while network.APs == []:
        count += 1
        if count > 10:
            raise Exception("Can't find any AP.")
        ps = subprocess.run(['iwlist', iface, 'scan'], capture_output=True)
        output = ps.stdout.decode().split("\n")
        for i in range(len(output)):
            if "Address" in output[i]:
                network.add_AP(AP(output[i][output[i].find(
                    ":")+2:], int(output[i+1][output[i+1].find(":")+1:]), []))


def set_channel(network, AP):
    try:
        print("Setting %s to channel %d" % (network.interface, AP.channel))
        subprocess.run(["iwconfig", network.interface,
                        "channel", str(AP.channel)], check=True)
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError(
            "Error setting %s to channel %d", network.interface, AP.channel)


def exit_handler():
    for iface in get_interfaces():
        managed_mode(iface)
        run_NetworkManeger()
