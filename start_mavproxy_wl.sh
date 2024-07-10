#! /bin/bash
## Executes MAVProxy so that you can connect the controller to the recognition program
## and another GCS in your computer.
## This script works when your computer is connected to the Jetson Nano's hotspot wirelessly.

mavproxy.py --master=/dev/ttyTHS1 --baudrate 57600 --out=udpbcast:10.42.0.255:14550 --out=udp:127.0.0.1:14550
