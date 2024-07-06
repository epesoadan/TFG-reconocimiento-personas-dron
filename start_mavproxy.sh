#! /bin/bash

mavproxy.py --master=/dev/ttyTHS1 --baudrate 57600 --out=udpbcast:192.168.1.255:14550 --out=udp:127.0.0.1:14550
