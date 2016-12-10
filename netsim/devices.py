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


class TriangulateLocationDevice(BaseDevice):
    # Message is defined as [x][y][timestamp]

    def __init__(self, propagation_speed, default_channel_id = 0, all_messages = []):
        self.propagation_speed = propagation_speed
        self.default_channel_id = default_channel_id
        self.all_messages = all_messages
        self.location = None

    def step(self, timestamp: float, messages_received: MessagesDict) \
            -> Tuple[MessagesDict, Position]:
        for message in messages_received[self.default_channel_id]:
            for saved_message in self.all_messages:
                if saved_message['Position']!=message['Position']:
                    self.all_messages.append(message)
            if len(self.all_messages) >= 3:
                if self.triangulate_helper(timestamp):
                    break
                else:
                    self.all_messages = []

    def triangulate_helper(self, timestamp):
        inputs = []
        for message in self.all_messages:
            position = message['Position']
            r = (timestamp - message['timestamp']) / self.propagation_speed
            inputs.append([position.x, position.y, r])
        triangulate_result = message_parser.triangulate(inputs[0]+inputs[1]+inputs[2])
        if triangulate_result != BAD_RESULT:
            self.location = triangulate_result
            return True
        else:
            return False
