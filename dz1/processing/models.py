from asyncio import events
from typing import List, Dict
import hashlib

class Event:
    start: float
    end: float
    file: str

    def __init__(self, start: float, end: float, file: str):
        self.start = start
        self.end = end
        self.file = file

    def __str__(self):
        return f"event of start: {self.start}, & end: {self.end} on file: {self.file}"

    def __hash__(self):
        m = hashlib.md5()
        m.update(repr(self.start).encode())
        m.update(repr(self.end).encode())
        m.update(self.file.encode())
        return int(m.hexdigest(), 16)


class Results:
    events: List[Event]
    calculations: Dict[int, Dict[str, Dict[str, float]]]

    def __repr__(self):
        return f"Results(events={self.events}, calculations={self.calculations})"