#!/usr/bin/env python3

import json
import unittest
import random
LIGHT_SPEED = 300000000
from .context import netsim

class GlobalLogger(object):
    def __init__(self):
        self.records = []

    def log(self, record):
        self.records.append(record)

    def dump(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.records, f)


class TestPropagatingIdentityChannel(unittest.TestCase):
    def setUp(self):
        self.propagation_speed = LIGHT_SPEED
        self.channel = netsim.PropagatingIdentityChannel('propagating_chan',
                                                         self.propagation_speed, 800)

    # def test_basic(self):
    #     device1 = netsim.StaticPingDevice('dev1', self.channel.id, netsim.Position(0, 0))
    #     device2 = netsim.StaticPingDevice('dev2', self.channel.id, netsim.Position(2, 0))
    #
    #     simulator = netsim.Simulator(0.5, [self.channel], [device1, device2])
    #     simulator.run(5)

    def test_triangulating(self):

        logger_t = GlobalLogger()

        try:

            device1 = netsim.StaticPingDevice('dev1', logger_t, self.channel.id, netsim.Position(100, 300))
            device2 = netsim.StaticPingDevice('dev2', logger_t, self.channel.id, netsim.Position(200, 200))
            device3 = netsim.StaticPingDevice('dev3', logger_t, self.channel.id, netsim.Position(0, 150))
            device_list = [device1, device2, device3]

            for i in range(0,50):
                lt_device1 = \
                    netsim.StaticLocationTriangulatingDevice('lt_dev' + str(i), logger_t, self.channel.id,
                                                             netsim.Position(random.random()*1000, random.random()*1000),
                                                             self.propagation_speed)
                device_list.append(lt_device1)

            
            simulator = netsim.Simulator(0.000000001, [self.channel], device_list)
            simulator.run(0.000003)
            logger_t.dump("hello1.txt")
            simulator.run(0.000006)
            logger_t.dump("hello2.txt")
            simulator.run(0.000009)
            logger_t.dump("hello3.txt")
            simulator.run(0.000012)
            logger_t.dump("hello4.txt")
            simulator.run(0.00003)
            logger_t.dump("hello5.txt")
            simulator.run(0.00009)
            logger_t.dump("hello6.txt")
        finally:
            logger_t.dump("hello.txt")
