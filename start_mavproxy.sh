#! /bin/bash
## Executes MAVProxy so that you can connect the controller to the recognition program
## and another GCS in your computer.
## This script works when the Jetson Nano is connected to your computer through
## a micro USB cable.

mavproxy.py --master=/dev/ttyTHS1 --baudrate 57600 --out=udpbcast:192.168.1.255:14550 --out=udp:127.0.0.1:14550
