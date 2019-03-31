from scapy.all import *


class AP:
    def __init__(self, BSSID, channel, clients):
        self.BSSID = BSSID
        self.channel = channel
        self.clients = clients

    def add_client(self, client):
        self.clients.append(client)

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
    
    def set_interface_mac(self, interface_mac):
        self.interface_mac = interface_mac

    def add_AP(self, AP):
        self.APs.append(AP)

    def add_client(self, BSSID, client):
        i = self.find_AP(BSSID)
        if i == -1:
            return
        self.APs[i].add_client(client)

    def get_AP(self, BSSID):
        i = self.find_AP(BSSID)
        if i == -1:
            return
        return self.APs[i]

    def find_AP(self, BSSID):
        i = -1
        for i in range(len(self.APs)):
            if self.APs[i].BSSID == BSSID:
                break
        return i
