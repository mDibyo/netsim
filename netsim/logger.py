import json


class GlobalLogger(object):
    def __init__(self):
        self.records = []

    def log(self, record):
        self.records.append(record)

    def dump(self, filename):
        with open(filename, 'w') as f:
            json.dump(f, self.records)
