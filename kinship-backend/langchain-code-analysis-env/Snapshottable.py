import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from Snapshot import Snapshot
from typing import Type, TypeVar
import inspect

Shoottable = TypeVar('Shoottable', bound='Snapshottable')


class Snapshottable(ABC):
    """
    An abstract class representing a snapshottable object that is stored in an immutable state whenever updates are made to it.
    """

    def __init__(self, subclass_type: Type, transaction_date) -> None:
        self.snapshots = []

        self.subclass_type = subclass_type
        self.uuid = uuid.uuid4()
        ### Define Subclass Behavior ###

        bound_methods = [getattr(self, x) for x in dir(self) if callable(getattr(self, x)) and not x.startswith('__')]
        superclass_methods = [getattr(superclass, method_name) for superclass in inspect.getmro(self.__class__)[:-1]
                              for method_name in dir(superclass) if callable(getattr(superclass, method_name))
                              and not method_name.startswith('__')]

        ### Define Attributes to Compare ###
        self.comparable_attributes = [attr_name for attr_name in dir(self) if not attr_name.startswith('__')
                                      and attr_name not in bound_methods
                                      and attr_name not in ['_abc_impl', 'snapshots', 'subclass_type', 'leases', 'unit', 'uuid']
                                      and getattr(self.__class__, attr_name, None) not in superclass_methods]

        ### Creation Shot ###
        self.take_snapshot(transaction_date=transaction_date)

    @abstractmethod
    def clone_without_snapshots(self):
        """
        Return a copy of the object without snapshots. To implement this, look an example on the Resident class.
        """

    def __eq__(self, other_object: Shoottable) -> bool:
        """
        Args:
            other_object: the object to compare with the context object

        Returns:
            True if they are equal, false if they are not
        """
        if not isinstance(other_object, self.subclass_type):
            return False
        else:
            attr_dict = self.__dict__
            attr_dict = {key: value for key, value in attr_dict.items() if key in self.comparable_attributes}
            for attr, value in attr_dict.items():
                other_value = getattr(other_object, attr)
                if isinstance(value, list):
                    if len(value) != len(other_value):
                        return False
                    for i in range(len(value)):
                        if value[i] != other_value[i]:
                            return False
                elif value != other_value:
                    return False
            return True

    def update_if_different(self, other_obj: Shoottable, transaction_date) -> Shoottable:
        """
        Update the current instance with the values of other_obj if they are the same type,
        but only if there is a difference. Also, creates and stores a snapshot of the instance after the update.
        The snapshot is only made if the update was made to a non-relationship attribute.

        Returns:
            self
        """
        update_occurred = False
        snapshot = None
        if not isinstance(other_obj, self.subclass_type):
            raise ValueError(f'Update_if_different function called to compare a {self.subclass_type} with a {type(other_obj)}')
        for attr_name in self.comparable_attributes:
            current_value = getattr(self, attr_name)
            other_value = getattr(other_obj, attr_name)
            if other_value is None:
                # print(f"other_value is None, skipping because we do not set attribute values to None after initialization")
                continue
            if isinstance(current_value, list):
                # Compare the lists element by element
                if len(current_value) != len(other_value):
                    raise ValueError(f'Cannot compare lists of different lengths: {len(current_value)} and {len(other_value)}')
                for i in range(len(current_value)):
                    update_occurred = self.compare_attr_values_and_update(attr_name, current_value[i], other_value[i], update_occurred,
                                                                          transaction_date)
            else:
                update_occurred = self.compare_attr_values_and_update(attr_name, current_value, other_value, update_occurred,
                                                                      transaction_date)
        if update_occurred:
            obj_without_snapshots = self.clone_without_snapshots()
            snapshot = Snapshot(obj=obj_without_snapshots, transaction_date=transaction_date, timestamp=datetime.now())
            del obj_without_snapshots
        if snapshot:
            self.snapshots.append(snapshot)
        return self


    def compare_attr_values_and_update(self, attr_name, current_value, other_value, update_occurred, transaction_date) -> bool:
        """
        Compare an attribute of the context class with another value for it and update it if the other value is different.This method is
        not designed to be passed an attribute that is a list. All attribute should be one of the following types before being passed in:
        Snapshottable, or python non-collection primitives like int, string, and bool.

        Args:
            attr_name: name of the attribute on the subclass of Snapshottable we are comparing for differences.
            current_value: the value of the attribute for the context instance
            other_value: the value of the attribute for the comparison instance
            update_occurred: boolean that would pass in as true if an update had already occurred and flipped to true if an update to a
            non-relationship occurred
            transaction_date: used to set the transaction_date of a snapshot instance

        Returns:
            update_occurred
        """
        if isinstance(current_value, Snapshottable):
            updated_obj = current_value.update_if_different(other_value, transaction_date=transaction_date)
            setattr(self, attr_name, updated_obj)
        elif current_value != other_value:
            update_occurred = True
            setattr(self, attr_name, other_value)
        return update_occurred

    def take_snapshot(self, transaction_date) -> None:
        """
        Take a snapshot of the current state of the object and add it to the list of snapshots.
        """
        snapshot = Snapshot(obj=self.clone_without_snapshots(), transaction_date=transaction_date, timestamp=datetime.now())
        self.snapshots.append(snapshot)

    def find_effective_snapshot(self, timestamp: datetime) -> Shoottable:
        # TODO: optimize this function with an optional parm to direct the search to start at a certain index
        # initializing bounds
        left = 0
        right = len(self.snapshots) - 1

        # binary search loop
        mid = 0
        while left <= right:
            mid = (left + right) // 2

            # comparing snapshot timestamp with timestamp parameter
            if self.snapshots[mid].transaction_date <= timestamp:
                left = mid + 1
            else:
                right = mid - 1

        # returning snapshot with latest transaction_date <= timestamp param
        return self.snapshots[mid]


