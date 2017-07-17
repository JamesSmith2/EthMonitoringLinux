#!/usr/bin/python

import json
import thread
import time
import httplib, urllib
from stats import Stats
from miners.ccminer_alexis import CCMinerAlexis
from miners.claymores import Claymores
from miners.ewbf import EWBF

from pprint import pprint

accessToken = ""

def sendToAPI(host, name, data):
    params = urllib.urlencode({'host': host, 'name': name, 'type': 2, 'version': '1.0', 'data': data, 'token': accessToken})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("ethmonitoring.com:80")
    conn.request("POST", "/api/update", params, headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

def monitorMiner(host, port, password, type, name):
    while 1:
        data = ""

        # Claymores dual miner
        if type == 0:
            data = Claymores(host, port, password).getStats()

        # CCMiner-Alexis type
        if type == 1:
            data = CCMinerAlexis(host, port, password).getStats()

        # EWBF type
        if type == 2:
            data = EWBF(host, port, password).getStats()

        # Update miner data
        sendToAPI(host, name, data)

        time.sleep(25)
        pass


with open('settings.json') as data_file:
    data = json.load(data_file)

try:
    accessToken = data["accessToken"]

    if len(accessToken) == 0:
        print("No access token defined")
        exit(0)

    if len(data["hosts"]) > 0:
        for miner in data["hosts"]:
            # Create two threads as follows
            try:
                thread.start_new_thread(monitorMiner, (miner['host'], miner['port'], miner['password'], miner['type'], miner['name']))
            except:
                print
                "Error: unable to start thread"
    else:
        pprint("No hosts found")
        exit(0)
except:
    print("Invalid config file")
    exit(1)

while 1:
    time.sleep(1)
    pass
