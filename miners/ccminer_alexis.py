#!/usr/bin/python

import json
import socket
import sys
from stats import Stats
from pprint import pprint


class CCMinerAlexis(object):
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.connected = 0

    def getCommand(self, command):
        try:
            # Create a TCP/IP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect the socket to the port where the server is listening
            server_address = (self.host, self.port)
            self.sock.connect(server_address)
            self.connected = 1

            # Send data
            self.sock.sendall(command)

            # receive data
            data = self.sock.recv(12000)

            # Close socket
            self.sock.close()

            return data

        except socket.error as msg:
            print("Socket error: {0}".format(msg))

    def getStats(self):
        data = Stats()
        data.type = 1

        try:
            summary_data = self.getCommand("summary|")
            summary_response = summary_data.split(";")

            if len(summary_response) > 0:
                data.version = summary_response[1].split("=")[1]
                data.total_hashrate = summary_response[5].split("=")[1]
                data.accepted = summary_response[7].split('=')[1]
                data.rejected = summary_response[8].split('=')[1]
                data.uptime = summary_response[14].split('=')[1]

            """ GPU RESPONSE """
            gpu_data = self.getCommand("threads|")
            gpu_response = gpu_data.split("|")

            if len(gpu_response) > 0:
                for gpu in gpu_response:
                    gpu_data = gpu.split(";")

                    if len(gpu_data) == 12:
                        hashrate = 0
                        wattage = 0

                        if data.version == "2.0":
                            hashrate = gpu_data[11].split('=')[1]
                            wattage = (int(gpu_data[4].split('=')[1]) / 1000)
                        else:
                            hashrate = gpu_data[8].split('=')[1]
                            wattage = (int(gpu_data[4].split('=')[1]) / 1000)

                            data.hashrates.append(hashrate)
                            data.temps.append(gpu_data[3].split('=')[1])
                            data.power_usage.append(wattage)
                            data.fan_speeds.append(gpu_data[5].split('=')[1])

            data.online = self.connected
        except:
            print("Data parsing error")

        return data.toJSON()
