#!/usr/bin/env python3


from abc import ABCMeta, abstractmethod
from typing import List, Dict

from .utils import Identifiable, Message, DevicePosition, MessagesDict


class AbstractChannel(Identifiable, metaclass=ABCMeta):
    @abstractmethod
    def step(self, timestamp: int, messages_inserted: List[Message],
             device_locations: Dict[str, DevicePosition]) -> MessagesDict:
        pass


class BaseChannel(AbstractChannel):
    def step(self, timestamp: int, messages_inserted: List[Message],
             device_locations: Dict[str, DevicePosition]) -> MessagesDict:
        return {device_id: messages_inserted for device_id in device_locations}


class ImmediateIdentityChannel(BaseChannel):
    pass
