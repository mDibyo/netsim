#!/usr/bin/env python3


import unittest

from .context import netsim


class TestPropagatingIdentityChannel(unittest.TestCase):
    def setUp(self):
        self.channel = netsim.PropagatingIdentityChannel('propagating_chan', 1)

    def test_basic(self):
        device1 = netsim.StaticPingDevice('dev2', self.channel.id, netsim.Position(0, 0))
        device2 = netsim.StaticPingDevice('dev1', self.channel.id, netsim.Position(2, 0))

        simulator = netsim.Simulator(0.5, [self.channel], [device1, device2])
        simulator.run(5)
