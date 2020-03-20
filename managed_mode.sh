ifconfig $1 down
iwconfig $1 mode managed
ifconfig $1 up
service NetworkManager restart
