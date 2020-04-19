# WIFI_Jammer

## Description

The application jams all reachable access points and their clients. First, it continuously sniffs packets to find access points and catch their clients. Then, it impersonates each access point and sends both generic and client-targeted deauth packets.<br/>The application is tested on Kali & Ubuntu Linux.<br/> All the following commands must be run as root.

## What's Special

* Object oriented design
* Containerized plug-and-play application

## Disclaimer

As per license, the developer is not liable for any misuse of this application. Deauthing WIFIs is a serious offense in some countries that is punishable by law.

## Build Docker image and run a container

* Navigate to root directory and build Docker image

```
docker build -f Dockerfile -t <tag_name> .
```

* Run Docker container. Please note that we first kill a process "wpa_supplicant" that might intervene with the attack

```
killall wpa_supplicant && docker run --privileged -it --net=host --mount src="$(pwd)",target="/WIFI_Jammer",type=bind <tag_name>
```
* After you stop the attack, run the below on your OS to restore normal wifi operation.
```
./managed_mode.sh --interface_name
```
## Usage

* Deauth all reachable access points

```
python3.7 run.py --all
```

* Deauth a specific access point
```
python3.7 run.py -b BSSID
```

you can skip a list of BSSIDs by adding -s BSSID1 BSSID2 ... when deauthing all APs.

## Planned features

* Ameliorate runtime messages
