#!/usr/bin/env python3


from collections import defaultdict, Hashable, namedtuple
from math import sqrt
from typing import DefaultDict, Any, Dict, List


class Identifiable(Hashable):
    def __init__(self, id_: str):
        self.id = id_

    def __hash__(self):
        return self.id

    def __str__(self):
        return '{class_} {id}'.format(class_=self.__class__, id=self.id)


def dict_list_merge_update(d: DefaultDict[Any, list], other: Dict[Any, list]) \
        -> DefaultDict[Any, list]:
    for channel_id, messages in other.items():
        d[channel_id].extend(messages)
    return d


Message = object


class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_from(self, other: 'Position'):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


origin = Position(0, 0)

MessagesDict = Dict[str, List[Message]]


def messages_dict() -> MessagesDict:
    return defaultdict(list)


class MessagePropagation(object):
    __slots__ = [
        'propagation_speed',
        'message',
        'origin_position',
        'timestamp',
        'propagation'
    ]

    def __init__(self, propagation_speed: float, message: Message,
                 origin_position: Position, timestamp: float):
        self.propagation_speed = propagation_speed  # type: float
        self.message = message  # type: Message
        self.origin_position = origin_position  # type: Position
        self.timestamp = timestamp  # timestamp: float
        self.propagation = 0  # type: float

    def step(self, timestamp: float):
        self.propagation += (timestamp - self.timestamp) \
                            * self.propagation_speed
        self.timestamp = timestamp


__all__ = [
    Identifiable,
    dict_list_merge_update,
    Message,
    Position, origin,
    MessagesDict, messages_dict,
    MessagePropagation
]
