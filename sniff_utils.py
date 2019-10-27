from scapy.all import *
from wifi_utils import *
from deauth_utils import *

ignore = []

def construct_ignore_list(skip):
    #check network mac, it may not be initialized.
    ignore = ["ff:ff:ff:ff:ff:ff", "00:00:00:00:00:00", "33:33:00:", "33:33:ff:", "01:80:c2:00:00:00", "01:00:5e:", network.interface_mac]
    if skip:
        ignore += [addr.lower() for addr in skip]


def noise_filter(addr1, addr2):
    for i in ignore:
        if i in addr1 or i in addr2:
            return True
    return False


def analyze_pkt(pkt):
    if pkt.haslayer(Dot11FCS):
        if pkt.addr1 and pkt.addr2:
            pkt.addr1 = pkt.addr1.lower()
            pkt.addr2 = pkt.addr2.lower()
        if noise_filter(pkt.addr1, pkt.addr2):
            return
        if pkt.type in [1, 2]:
            print(pkt.addr1)
            # network.add_client(pkt.addr2, pkt.addr1)

try:
    sniff(iface="wlan0", store=False, prn = analyze_pkt)
except Exception as e:
    print(str(e))
