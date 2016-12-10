#!/usr/bin/env python3


from abc import ABCMeta, abstractmethod
from typing import Tuple

from .utils import *


class AbstractDevice(Identifiable, metaclass=ABCMeta):
    @abstractmethod
    def step(self, timestamp: float, messages_received: MessagesDict) \
            -> Tuple[MessagesDict, Position]:
        pass


class BaseDevice(AbstractDevice):
    def step(self, timestamp: float, messages_received: MessagesDict) \
            -> Tuple[MessagesDict, Position]:
        return {}, origin


class StaticPingDevice(BaseDevice):
    def __init__(self, id_, channel_id, position: Position):
        super(StaticPingDevice, self).__init__(id_)

        self.channel_id = channel_id
        self.position = position

    def step(self, timestamp: float, messages_received: MessagesDict) \
            -> Tuple[MessagesDict, Position]:
        print(messages_received)

        return {self.channel_id: ['ping']}, self.position
