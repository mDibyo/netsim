#!/usr/bin/env python3


from collections import defaultdict, namedtuple, Hashable
from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Dict


Message = object


class Identifiable(Hashable):
    def __init__(self, id_: str):
        self.id = id_

    def __hash__(self):
        return self.id

    def __str__(self):
        return '{class_} {id}'.format(class_=self.__class__, id=self.id)


class AbstractChannel(Identifiable, metaclass=ABCMeta):
    @abstractmethod
    def step(self, timestamp: int, messages_inserted: List[Message]) \
            -> List[Message]:
        pass


class BaseChannel(AbstractChannel):
    def step(self, timestamp: int, messages_inserted: List[Message]) \
            -> List[Message]:
        return messages_inserted


class ImmediateIdentityChannel(BaseChannel):
    pass


ChannelMessagesDict = Dict[str, List[Message]]


def channel_messages_dict_merge_update(
    d: ChannelMessagesDict,
    other: ChannelMessagesDict
) -> ChannelMessagesDict:
    for channel_id, messages in other.items():
        d[channel_id].extend(messages)

    return d


DevicePosition = namedtuple('DevicePosition', ['x', 'y'])
origin = DevicePosition(0, 0)


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
