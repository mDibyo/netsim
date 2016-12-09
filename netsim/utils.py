#!/usr/bin/env python3


from collections import namedtuple, Hashable
from typing import DefaultDict, Any, Dict, List


class Identifiable(Hashable):
    def __init__(self, id_: str):
        self.id = id_

    def __hash__(self):
        return self.id

    def __str__(self):
        return '{class_} {id}'.format(class_=self.__class__, id=self.id)


def dict_merge_update(d: DefaultDict[Any, list], other: Dict[Any, list]) \
        -> DefaultDict[Any, list]:
    for channel_id, messages in other.items():
        d[channel_id].extend(messages)
    return d


Message = object
DevicePosition = namedtuple('DevicePosition', ['x', 'y'])
MessagesDict = Dict[str, List[Message]]
origin = DevicePosition(0, 0)
