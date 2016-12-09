#!/usr/bin/env python3


from abc import ABCMeta, abstractmethod
from typing import Tuple

from .utils import *


class AbstractDevice(Identifiable, metaclass=ABCMeta):
    @abstractmethod
    def step(self, timestamp: int, messages_received: List[Message]) \
            -> Tuple[MessagesDict, DevicePosition]:
        pass


class BaseDevice(AbstractDevice):
    def step(self, timestamp: int, messages_received: List[Message]) \
            -> Tuple[MessagesDict, DevicePosition]:
        return {}, origin


class StaticOriginBlackHoleDevice(BaseDevice):
    pass


def StaticOriginPingDeviceFactory(channel_id: str):
    class StaticOriginPingDevice(BaseDevice):
        def step(self, timestamp: int, messages_received: List[Message]) \
                -> Tuple[MessagesDict, DevicePosition]:
            return {channel_id: [0]}, origin

    return StaticOriginPingDevice
