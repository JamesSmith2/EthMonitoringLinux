#!/usr/bin/python

import json
import socket
import sys
from stats import Stats
from pprint import pprint


class EWBF(object):
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.connected = 0

    def getData(self):
        try:
            # Create a TCP/IP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect the socket to the port where the server is listening
            server_address = (self.host, self.port)
            self.sock.connect(server_address)
            self.connected = 1

            command = "{\"id\":1, \"method\":\"getstat\"}\n"

            # Send data
            self.sock.sendall(command)

            # receive data
            data = self.sock.recv(12000)

            print
            "DATA: %s" % data

            # Close socket
            self.sock.close()

            return data

        except socket.error as msg:
            print("Socket error: {0}".format(msg))

    def getStats(self):
        data = Stats()
        data.type = 2
        try:
            summary_data = self.getData()
            result = json.loads(summary_data)

            summary_response = result["result"]
            total_hashrate = 0
            data.version = "EWBF"

            for gpu in summary_response:
                # Speed
                data.hashrates.append(gpu["speed_sps"]);
                data.power_usage.append(gpu["gpu_power_usage"]);
                data.fan_speeds.append("0");
                data.temps.append(gpu["temperature"]);
                total_hashrate += gpu["speed_sps"];

                # Shares
                data.accepted += gpu["accepted_shares"];
                data.rejected += gpu["rejected_shares"];

            data.total_hashrate = str(total_hashrate);
            data.online = self.connected
        except:
            print("paring error")

        return data.toJSON()
