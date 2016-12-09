#!/usr/bin/env python3


from collections import defaultdict

from .channels import BaseChannel
from .devices import BaseDevice
from .utils import *


class Simulator(object):
    def __init__(self, step_size: float, channels: List[BaseChannel],
                 devices: List[BaseDevice]):
        self.step_size = step_size

        self.channels = channels
        self.devices = devices

        self.next_timestamp = 0
        self.messages_to_insert = defaultdict(list)
        self.device_positions = {}

    def step(self):
        messages_received = defaultdict(list)
        for channel in self.channels:
            device_messages = channel.step(
                self.next_timestamp, self.messages_to_insert[channel.id],
                self.device_positions)
            dict_merge_update(messages_received, device_messages)

        self.messages_to_insert = defaultdict(list)
        for device in self.devices:
            channel_messages, position = \
                device.step(self.next_timestamp, messages_received[device.id])
            dict_merge_update(self.messages_to_insert, channel_messages)
            self.device_positions[device.id] = position

        self.next_timestamp += self.step_size

    def run(self, till):
        while self.next_timestamp <= till:
            self.step()


if __name__ == '__main__':
    simulator = Simulator(0.000001, [], [])
    simulator.run(1)

