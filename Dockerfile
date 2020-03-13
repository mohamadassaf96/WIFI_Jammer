FROM ubuntu:18.04

#install dependencies.
RUN apt-get update && apt-get install -y \
  locales \
  python3.7 \
  python3-pip \
  pkg-config \
  zip \
  net-tools \
  aircrack-ng \
  g++ \
  zlib1g-dev \
  git-core \
  python-minimal \
  && python3.7 -m pip install scapy
