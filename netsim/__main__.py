#!/usr/bin/env python3


from .channels import BaseChannel
from .devices import BaseDevice
from .utils import *


class Simulator(object):
    def __init__(self, step_size: float, channels: List[BaseChannel],
                 devices: List[BaseDevice]):
        self.step_size = step_size

        self.channels = channels
        self.devices = devices

        self.next_timestamp = 0  # type: int
        self.messages_to_insert = defaultdict(messages_dict)
        self.device_positions = {}

    def step(self):
        messages_received = messages_dict()
        for channel in self.channels:
            device_messages = channel.step(
                self.next_timestamp, self.messages_to_insert[channel.id],
                self.device_positions)
            dict_list_merge_update(messages_received, device_messages)

        self.messages_to_insert = defaultdict(messages_dict)
        for device in self.devices:
            channel_messages, self.device_positions[device.id] = \
                device.step(self.next_timestamp, messages_received[device.id])
            for channel_id, messages in channel_messages:
                self.messages_to_insert[channel_id][device.id].extend(messages)

        self.next_timestamp += self.step_size

    def run(self, till):
        while self.next_timestamp <= till:
            self.step()


if __name__ == '__main__':
    simulator = Simulator(0.000001, [], [])
    simulator.run(1)

