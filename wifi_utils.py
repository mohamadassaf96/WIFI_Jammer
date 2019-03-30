import os
import subprocess
import time
import atexit

DN = open(os.devnull, 'w')

def get_interfaces():
    interfaces = []
    try:
        iwcofig_cmd = subprocess.Popen(["iwconfig"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
    ps = subprocess.Popen(('iwconfig', iface), stdout=subprocess.PIPE)
    output = subprocess.check_output(('grep', 'Mode'), stdin=subprocess.Popen(('iwconfig', iface), stdout=subprocess.PIPE).stdout)
    if "Monitor" in output.decode():
        print(iface + " in monitor mode.")

def managed_mode(iface):
    try:
        subprocess.run(["ifconfig", iface, "down"], check=True)
        subprocess.run(["iwconfig", iface, "mode", "managed"], check=True)
        subprocess.run(["ifconfig", iface, "up"], check=True)
    except:
        raise Exception("Cannot set interface to managed mode.")
    output = subprocess.check_output(('grep', 'Mode'), stdin=subprocess.Popen(('iwconfig', iface), stdout=subprocess.PIPE).stdout)
    if "Managed" in output.decode():
        print(iface + " in managed mode.")

def run_NetworkManeger():
    try:
        subprocess.run(["service", "NetworkManager", "restart"], check=True)
    except:
        raise Exception("Cannot start NetworkManager service.")

def iwlist_scan(iface):
    APs = {}
    count = 0
    output = subprocess.check_output(('grep', 'Mode'), stdin=subprocess.Popen(('iwconfig', iface), stdout=subprocess.PIPE).stdout)
    if "Monitor" in output.decode():
        managed_mode([iface])
    while APs == {}:
        count+=1
        if count > 10:
            raise Exception("Can't find any AP.")
        ps = subprocess.run(['iwlist', iface, 'scan'], capture_output=True)
        output = ps.stdout.decode().split("\n")
        for i in range(len(output)):
            if "Address" in output[i]:
                APs[output[i][output[i].find(":")+2:]] = int(output[i+1][output[i+1].find(":")+1:])
    return APs

def set_channel(iface, channel):
    try:
        print("Setting %s to channel %d" % (iface, channel))
        subprocess.run(["iwconfig", "wlan0", "channel", str(channel)], check=True)
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError("Error setting %s to channel %d", iface, channel)

def exit_handler():
    for iface in get_interfaces():
        managed_mode(iface)
        run_NetworkManeger()