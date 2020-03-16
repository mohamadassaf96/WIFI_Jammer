FROM ubuntu:18.04

#install dependencies.
RUN apt-get update && apt-get install -y \
  python3.7 \
  python3-pip \
  net-tools \
  wireless-tools \
  aircrack-ng \
  pciutils \
  && python3.7 -m pip install scapy

WORKDIR WIFI_Jammer/