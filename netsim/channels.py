#!/usr/bin/env python3


from abc import ABCMeta, abstractmethod
from functools import reduce
from typing import List, Dict

from .utils import *


class AbstractChannel(Identifiable, metaclass=ABCMeta):
    @abstractmethod
    def step(self, timestamp: float, messages_inserted: List[Message],
             device_locations: Dict[str, Position]) -> MessagesDict:
        pass


class BaseChannel(AbstractChannel):
    def step(self, timestamp: float, device_messages_inserted: MessagesDict,
             device_locations: Dict[str, Position]) -> MessagesDict:
        messages_inserted = reduce(lambda a, b: a + b,
                                   device_messages_inserted.values())
        return {device_id: messages_inserted for device_id in device_locations}


class ImmediateIdentityChannel(BaseChannel):
    pass


class PropagatingIdentityChannel(BaseChannel):
    def __init__(self, id_, propagation_speed):
        super(PropagatingIdentityChannel, self).__init__(id_)

        self.propagation_speed = propagation_speed # type: float
        self.device_positions = {}  # type: Dict[str, Position]
        self.message_propagations = []  # type: List[MessagePropagation]
        self.prev_timestamp = 0  # type: float

    def step(self, timestamp: float, devices_messages_inserted: MessagesDict,
             new_device_positions: Dict[str, Position]) -> MessagesDict:
        self.device_positions.update(new_device_positions)

        message_to_receive = messages_dict()
        for message_propagation in self.message_propagations:
            prev_propagation = message_propagation.propagation
            message_propagation.step(timestamp)
            for device_id, position in self.device_positions.items():
                distance = \
                    position.distance_from(message_propagation.origin_position)
                if prev_propagation < distance <= message_propagation.propagation:
                    message_to_receive[device_id].append(message_propagation.message)

        self.prev_timestamp = timestamp
        for device_id, messages in devices_messages_inserted.items():
            assert device_id in self.device_positions

            self.message_propagations.extend(MessagePropagation(
                self.propagation_speed,
                m,
                self.device_positions[device_id],
                timestamp
            ) for m in messages)

        return message_to_receive
