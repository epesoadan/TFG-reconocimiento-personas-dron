#! /bin/bash

mavproxy.py --master=/dev/ttyTHS1 --baudrate 57600 --out=udpbcast:10.42.0.255:14550 --out=udp:127.0.0.1:14550
