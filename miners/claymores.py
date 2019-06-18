#!/usr/bin/python

import json
import socket
import sys
from stats import Stats
from pprint import pprint


class Claymores(object):
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

            if self.password is not None:
                command = "{\"id\":0,\"jsonrpc\":\"2.0\",\"method\":\"miner_getstat1\",\"psw\":\"" + str(
                    self.password) + "\"}"
            else:
                command = "{\"id\":0,\"jsonrpc\":\"2.0\",\"method\":\"miner_getstat1\"}"

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
        data.type = 0
        try:
            summary_data = self.getData()
            result = json.loads(summary_data)

            summary_response = result["result"]
            miner_stats = summary_response[2].split(";")

            data.version = summary_response[0]
            data.uptime = summary_response[1]

            if len(miner_stats) > 0:
                data.total_hashrate = miner_stats[0]
                data.accepted = miner_stats[1]
                data.rejected = miner_stats[2]

            dual_stats = summary_response[4].split(";")
            if len(dual_stats) > 0:
                data.total_dual_hashrate = dual_stats[0]
                data.dual_accepted = dual_stats[1]
                data.dual_rejected = dual_stats[2]

            data.hashrates = summary_response[3].split(';');  # ETH hashrates
            data.dcr_hashrates = summary_response[5].split(';');  # DCR Hashrates

            # Temps and fan speeds
            temp = summary_response[6].split(';')
	    i = 0
	    while i < len(temp) - 1:
                data.temps.append(temp[i])
                data.fan_speeds.append(temp[i + 1])
		i += 2

            data.online = self.connected
        except Exception, e:
            print("Parsing error: " + str(e))

        return data.toJSON()
