# WIFI_Jammer

## Description

The application jams all reachable access points and their clients. First, it continuously sniffs packets to find access points and catch their clients. Then, it impersonates each access point and sends both generic and client-targeted deauth packets.<br/>The application is tested on Kali & Ubuntu Linux.<br/> All the following commands must be run as root.

## What's Special

* Object oriented design
* Containerized plug-and-play application

## Build Docker Image

Navigate to root directory

```
docker build -f Dockerfile -t <tag_name> .
```

## Run Docker Container

Navigate to root directory

```
killall wpa_supplicant && docker run --privileged -it --net=host --mount src="$(pwd)",target="/WIFI_Jammer",type=bind <tag_name>
```

## Usage

* Deauth all reachable access points

```
python3.7 script.py --all
```

* Deauth a specific access point
```
python3.7 script.py -b BSSID
```

you can skip a list of BSSIDs by adding -s BSSID1 BSSID2 ... when deauthing all APs.

## Planned features

* Ameliorate runtime messages
