#!/usr/bin/env python3


from collections import Hashable, namedtuple
from abc import ABCMeta, abstractmethod
from typing import List, Tuple


class Message(dict):
    pass


class AbstractChannel(Hashable, metaclass=ABCMeta):
    @abstractmethod
    def step(self, timestamp: int, messages_inserted: List[Message]) -> List[Message]:
        pass


class IdentifiableChannel(AbstractChannel, metaclass=ABCMeta):
    def __init__(self, id_: str):
        self.id = id_

    def __hash__(self):
        return self.id


class ImmediateIdentityChannel(IdentifiableChannel):
    def step(self, timestamp: int, messages_inserted: List[Message]) -> List[Message]:
        return messages_inserted


DevicePosition = namedtuple('DevicePosition', ['x', 'y'])


class Device(Hashable, metaclass=ABCMeta):
    @abstractmethod
    def step(self, timestamp: int, messages_received: List[Message]) -> Tuple[List[Message], DevicePosition]:
        pass


