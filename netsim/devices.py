#!/usr/bin/env python3


from abc import ABCMeta, abstractmethod
from typing import Tuple

from .utils import *
from .message_parser import triangulate, BAD_RESULT


class AbstractDevice(Identifiable, metaclass=ABCMeta):
    @abstractmethod
    def step(self, timestamp: float, messages_received: MessagesDict) \
            -> Tuple[MessagesDict, Position]:
        pass


class BaseDevice(AbstractDevice):
    def step(self, timestamp: float, messages_received: MessagesDict) \
            -> Tuple[MessagesDict, Position]:
        return {}, origin


class LoggingDevice(BaseDevice):
    def __init__(self, id_, logger):
        super(LoggingDevice, self).__init__(id_)
        self.logger = logger


class StaticPingDevice(LoggingDevice):
    def __init__(self, id_, logger, channel_id, position: Position):
        super(StaticPingDevice, self).__init__(id_, logger)

        self.channel_id = channel_id
        self.position = position

    def step(self, timestamp: float, messages_received: MessagesDict) \
            -> Tuple[MessagesDict, Position]:
        # print(messages_received[self.channel_id])

        return {self.channel_id: [{
            'position': self.position,
            'timestamp': timestamp
        }]}, self.position


class StaticLocationTriangulatingDevice(StaticPingDevice):
    def __init__(self, id_, logger, channel_id, position,
                 propagation_speed):
        super(StaticLocationTriangulatingDevice, self).__init__(id_, logger,
                                                                channel_id, position)

        self.propagation_speed = propagation_speed
        self.all_messages = []
        self.calculated_position = None
        self.saved_position_keys = set()

    def step(self, timestamp: float, messages_received: MessagesDict) \
            -> Tuple[MessagesDict, Position]:
        if self.calculated_position is None:
            for message in messages_received[self.channel_id]:
                position = message['position']
                if position.key() in self.saved_position_keys:
                    continue

                self.saved_position_keys.add(position.key())
                self.all_messages.append((position.x, position.y,
                                          (timestamp - message['timestamp']) * self.propagation_speed))

            if len(self.all_messages) >= 3:
                if not self.triangulate_helper(timestamp):
                    self.all_messages = []
                    self.saved_position_keys = set()

        if self.calculated_position is not None:
            return {self.channel_id: [{
                'position': self.calculated_position,
                'timestamp': timestamp
            }]}, self.position

        return {}, self.position

    def triangulate_helper(self, timestamp):
        inputs = self.all_messages[:3]
        triangulate_result = triangulate(*inputs[0], *inputs[1], *inputs[2])
        # print('tr', triangulate_result)
        if triangulate_result != BAD_RESULT:
            self.calculated_position = triangulate_result
            print (self.position.key())
            print (self.calculated_position)
            self.logger.log('\n\noriginal: ')
            self.logger.log(str(self.position.key()))
            self.logger.log(' | calculate: ')
            self.logger.log(self.calculated_position)
            self.logger.log(' | time: ')
            self.logger.log(timestamp)
            return True

        return False
