#!/usr/bin/env python3


from collections import defaultdict, namedtuple, Hashable
from abc import ABCMeta, abstractmethod
from typing import Any, List, Tuple, Dict, DefaultDict


DevicePosition = namedtuple('DevicePosition', ['x', 'y'])
origin = DevicePosition(0, 0)
Message = object
DeviceMessagesDict = Dict[str, List[Message]]


class Identifiable(Hashable):
    def __init__(self, id_: str):
        self.id = id_

    def __hash__(self):
        return self.id

    def __str__(self):
        return '{class_} {id}'.format(class_=self.__class__, id=self.id)


class AbstractChannel(Identifiable, metaclass=ABCMeta):
    @abstractmethod
    def step(self, timestamp: int, messages_inserted: List[Message],
             device_locations: Dict[str, DevicePosition]) -> DeviceMessagesDict:
        pass


class BaseChannel(AbstractChannel):
    def step(self, timestamp: int, messages_inserted: List[Message],
             device_locations: Dict[str, DevicePosition]) -> DeviceMessagesDict:
        return {device_id: messages_inserted for device_id in device_locations}


class ImmediateIdentityChannel(BaseChannel):
    pass


ChannelMessagesDict = Dict[str, List[Message]]


def dict_merge_update(d: DefaultDict[Any, list], other: Dict[Any, list]) \
        -> DefaultDict[Any, list]:
    for channel_id, messages in other.items():
        d[channel_id].extend(messages)
    return d


class AbstractDevice(Identifiable, metaclass=ABCMeta):
    @abstractmethod
    def step(self, timestamp: int, messages_received: List[Message]) \
            -> Tuple[ChannelMessagesDict, DevicePosition]:
        pass


class BaseDevice(AbstractDevice):
    def step(self, timestamp: int, messages_received: List[Message]) \
            -> Tuple[ChannelMessagesDict, DevicePosition]:
        return {}, origin


class StaticOriginBlackHoleDevice(BaseDevice):
    pass


def StaticOriginPingDeviceFactory(channel_id: str):
    class StaticOriginPingDevice(BaseDevice):
        def step(self, timestamp: int, messages_received: List[Message]) \
                -> Tuple[ChannelMessagesDict, DevicePosition]:
            return {channel_id: [0]}, origin

    return StaticOriginPingDevice


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
