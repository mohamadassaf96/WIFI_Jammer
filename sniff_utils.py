from scapy.all import *
from wifi_utils import *
from deauth_utils import *

ignore = []

def construct_ignore_list(skip):
    #check network mac, it may not be initialized.
    global ignore
    ignore = ["ff:ff:ff:ff:ff:ff", "00:00:00:00:00:00", "33:33:00:", "33:33:ff:", "01:80:c2:00:00:00", "01:00:5e:", network.interface_mac]
    if skip:
        ignore += [addr.lower() for addr in skip]

def noise_filter(addr1, addr2):
    for i in ignore:
        if i==addr1 or i==addr2:
            return True
    return False


def analyze_pkt(pkt):
    if not pkt.haslayer(Dot11FCS):
        return
    
    if pkt.addr1 is None or pkt.addr2 is None:
        return
        
    if pkt.haslayer(Dot11FCS):
        if pkt.addr1 and pkt.addr2:
            pkt.addr1 = pkt.addr1.lower()
            pkt.addr2 = pkt.addr2.lower()

        if noise_filter(pkt.addr1, pkt.addr2):
            return

        if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
            add_AP(pkt)

        if pkt.type in [1, 2]:
            add_client(pkt)

def add_client(pkt):
    network.add_client(pkt.addr2.lower(), pkt.addr1.lower())    

def add_AP(pkt):
    bssid = pkt.addr3.lower()
    try:
        ap_channel = str(ord(pkt[Dot11Elt:3].info))
    except:
        return
    network.add_AP_BSSID(bssid, ap_channel)

def launch_sniffing(skip):
    construct_ignore_list(skip)
    count = 0
    while (count < 10):
        count = count + 1
        try:
            sniff(iface=network.interface_name, store=False, prn = analyze_pkt)
        except Exception as e:
            print(str(e))
    raise Exception("Cannot launch packet sniffing, aborting ...")
