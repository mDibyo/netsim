#!/usr/bin/env python3


import unittest

from .context import netsim


class TestPropagatingIdentityChannel(unittest.TestCase):
    def setUp(self):
        self.propagation_speed = 2
        self.channel = netsim.PropagatingIdentityChannel('propagating_chan',
                                                         self.propagation_speed)

    # def test_basic(self):
    #     device1 = netsim.StaticPingDevice('dev1', self.channel.id, netsim.Position(0, 0))
    #     device2 = netsim.StaticPingDevice('dev2', self.channel.id, netsim.Position(2, 0))
    #
    #     simulator = netsim.Simulator(0.5, [self.channel], [device1, device2])
    #     simulator.run(5)

    def test_triangulating(self):

        # device1 = netsim.StaticPingDevice('dev1', self.channel.id, netsim.Position(1, 2))
        # device2 = netsim.StaticPingDevice('dev2', self.channel.id, netsim.Position(2, 3))
        # device3 = netsim.StaticPingDevice('dev3', self.channel.id, netsim.Position(4, 4))
        device1 = netsim.StaticPingDevice('dev1', self.channel.id, netsim.Position(-1, 0))
        device2 = netsim.StaticPingDevice('dev2', self.channel.id, netsim.Position(1, 0))
        device3 = netsim.StaticPingDevice('dev3', self.channel.id, netsim.Position(0, 1))

        lt_device1 = \
            netsim.StaticLocationTriangulatingDevice('lt_dev1', self.channel.id,
                                                     netsim.Position(0, 0),
                                                     self.propagation_speed)

        simulator = netsim.Simulator(0.001, [self.channel], [
            device1,
            device2,
            device3,
            lt_device1
        ])
        simulator.run(3)

        print(lt_device1.calculated_position)
