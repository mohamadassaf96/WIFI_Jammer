from scapy.all import *
from wifi_utils import *
from deauth_utils import *


def noise_filter(addr1, addr2):
    ignore = ['ff:ff:ff:ff:ff:ff', '00:00:00:00:00:00', '33:33:00:',
              '33:33:ff:', '01:80:c2:00:00:00', '01:00:5e:']
    for i in ignore:
        if i in addr1 or i in addr2:
            return True
    return False


def analyze_pkt(pkt):
    if pkt.haslayer(Dot11):
        if pkt.addr1 and pkt.addr2:
            print(pkt.addr1)
            pkt.addr1 = pkt.addr1.lower()
            pkt.addr2 = pkt.addr2.lower()
        if noise_filter(pkt.addr1, pkt.addr2):
            return
        if pkt.type in [1, 2]:
            print(pkt.addr1)
            # network.add_client(pkt.addr2, pkt.addr1)


def PacketHandler(packet):
    if packet.haslayer(Dot11):
        if packet.type == 0 and packet.subtype == 8:
                print("Access Point MAC: %s with SSID: %s " %(packet.addr2, packet.info))

iwlist_scan("wlan0")
prepare_attack()
atexit.register(exit_handler)
try:
    while (1):
        sniff(iface="wlan0", store=False, prn = PacketHandler, count=1)
except Exception as e:
    print(str(e))
