from datetime import datetime
from dataclasses import dataclass



@dataclass(frozen=True)
class Snapshot:
    """
    An abstract class representing a snapshot of a mutable object that can be stored in an immutable state.
    """
    obj: object
    transaction_date: datetime
    timestamp: datetime

    def __eq__(self, other):
        if isinstance(other, Snapshot):
            return self.transaction_date == other.transaction_date
        return False

    def __gt__(self, other):
        if isinstance(other, Snapshot):
            return self.transaction_date > other.transaction_date
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Snapshot):
            return self.transaction_date < other.transaction_date
        return NotImplemented

