# WIFI_Jammer

## Description

The application jams all reachable access points and their clients. First, it scans the network and gets all access points --will be deprecated, Second, continuously sniff packets to find additional access points and catch their clients. Finally it impersonates each access points and sends both generic and client-targeted deauth packets.
All the following commands must be run as root.

## Prerequisites

* python 3.7

```
apt-get install python3
```

* scapy

```
pip3 install scapy
```

## Usage

* Deauth all reachable access points

```
python3 script.py --all
```

* Deauth a specific access point
```
python3 script.py -b BSSID
```

you can skip a list of BSSIDs by adding -s BSSID1 BSSID2 ... when deauthing all APs.

## Planned features

* Implement a Docker container for the application
* Ameliorate runtime messages
