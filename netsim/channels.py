#!/usr/bin/env python3


from abc import ABCMeta, abstractmethod
from functools import reduce

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


class PropagatingChannel(BaseChannel):
    def __init__(self, id_, propagation_speed):
        super(PropagatingChannel, self).__init__(id_)

        self.propagation_speed = propagation_speed # type: float
        self.device_locations = {}  # type: Dict[str, Position]
        self.message_propagations = []  # type: List[MessagePropagation]
        self.prev_timestamp = 0  # type: float

    def step(self, timestamp: float, devices_messages_inserted: MessagesDict,
             new_device_locations: Dict[str, Position]) -> MessagesDict:
        old_device_locations = self.device_locations
        self.device_locations = {}\
            .update(old_device_locations)\
            .update(old_device_locations)

        message_to_receive = messages_dict()
        for propagation in self.message_propagations:
            # TODO(dibyo): Implement message propagation.
            print(propagation.message)

        for device_id, messages in devices_messages_inserted.items():
            assert device_id in self.device_locations

            self.message_propagations.extend(
                MessagePropagation(m, self.device_locations[device_id], timestamp)
                for m in messages)

        return message_to_receive
