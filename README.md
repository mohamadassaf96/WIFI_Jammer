# wifi_jammer

All the following must be run as root.

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
