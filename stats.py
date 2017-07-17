#!/usr/bin/python
import json

class Stats(object):
    def __init__(self):
        """Return a new Truck object."""
        self.version = ""
        self.total_hashrate = ""
        self.total_dual_hashrate = ""
        self.type = 0
        self.hashrates = []
        self.dcr_hashrates = []
        self.temps = []
        self.fan_speeds = []
        self.power_usage = []
        self.online = 0
        self.uptime = ""

        """pool stats"""
        self.accepted = 0
        self.rejected = 0
        self.dual_accepted = 0
        self.dual_rejected = 0

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

