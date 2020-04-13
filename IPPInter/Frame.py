"""
    VUT FIT IPP 2019/2020 project.
    Author: Ing. Juraj Lahvička
    2020
"""

import copy
from abc import abstractmethod, ABC

from IPPInter.Argument import Argument
from IPPInter.InterpretCustomExceptions import *


class FrameBase(ABC):
    """Frame base class."""
    _dict = None

    def __init__(self, name):
        self._name = name

    def init(self):
        self._dict = dict()

    def clear(self):
        self._dict = None

    @abstractmethod
    def get(self, item: Argument):
        self.__check_stack_init__()
        self.__check_existence__(item.value)

    def __check_stack_init__(self):
        if self._dict is None:
            raise FrameDoesNotExistError(self._name)

    def __check_existence__(self, item):
        """Check if the item is in dictionary"""
        if self._dict.get(item) is None:
            raise VarDoesNotExistsExc(self._name + str(item))

    def __str__(self) -> str:
        return self._dict.__str__()

    @property
    def name(self):
        return self._name


class Frame(FrameBase):
    """
        Frame class that represents frame and inherits from Frame base.
        Items are saved into Frame private dictionary like this {'var_name': ('var_type', var_value)}
    """

    MaxInitVars = 0

    def add(self, item: Argument):
        """Method for adding argument (values needed from argument) into frame."""
        self.__check_stack_init__()
        if self._dict.get(item.value):
            raise Redefinition(item.value)

        self._dict[item.value] = (item.i_type, None)

    def get(self, item: Argument, check_init=True):
        """Returns desired item from Frame."""
        super().get(item)
        if check_init:
            self.__check_var_init__(item.value)
        return self._dict[item.value]

    def assign(self, to: Argument, other_type, other_value):
        """Assign value into appropriate item."""
        self.__check_stack_init__()
        self.__check_existence__(to.value)

        if self.MaxInitVars < len(self._dict):
            if self._dict[to.value][0] == Argument.Non_term_var and self._dict[to.value][1] is None:
                self.MaxInitVars += 1

        self._dict[to.value] = (other_type, other_value)

    def replace(self, other: "Frame"):
        """Replace the whole Frame with other Frame. It swaps the private dictionaries."""
        other.__check_stack_init__()

        if other.MaxInitVars > self.MaxInitVars:
            self.MaxInitVars = other.MaxInitVars

        self._dict = other._dict

    def __check_var_init__(self, item):
        i_type, val = self._dict[item]
        if val is None and i_type == Argument.Non_term_var:
            raise MissingValue(item)


class LocalFrame:
    """
        Local Frame class represents the Local Frame.
        The local Frame is list of Frames. It points to the top frame.
    """

    MaxInitVars = 0

    _stack = None

    def __init__(self):
        self._name = "LF"

    def init(self):
        self._stack = list()

    def clear(self):
        self._stack = None

    def add(self, item: Argument):
        """Method for adding argument (values needed from argument) into top Frame."""
        self.__check_stack_init__()
        self.__check_stack_empty__()
        self._stack[len(self._stack) - 1].add(item)

        max_init_vars_sum = self.__gather_vars__()
        if max_init_vars_sum > self.MaxInitVars:
            self.MaxInitVars = max_init_vars_sum

    def get(self, item: Argument, check_init=True):
        """Returns desired item from top Frame."""
        self.__check_stack_init__()
        self.__check_stack_empty__()
        return self._stack[len(self._stack) - 1].get(item, check_init)

    def push(self, frame: "Frame"):
        """Makes deep copy from the frame and adds it to top."""
        self.__check_stack_init__()
        frame.__check_stack_init__()

        max_init_vars_sum = self.__gather_vars__() + frame.MaxInitVars
        if max_init_vars_sum > self.MaxInitVars:
            self.MaxInitVars = max_init_vars_sum

        self._stack.append(copy.deepcopy(frame))

    def pop(self) -> Frame:
        self.__check_stack_init__()
        self.__check_stack_empty__()
        return self._stack.pop()

    def assign(self, to: Argument, other_type, other_value):
        """Assign value into appropriate item in top frame."""
        self.__check_stack_init__()
        self.__check_stack_empty__()
        self._stack[len(self._stack) - 1].assign(to, other_type, other_value)

    def __check_stack_empty__(self):
        if len(self._stack) == 0:
            raise FrameDoesNotExistError(self._name)

    def __check_stack_init__(self):
        if self._stack is None:
            raise FrameDoesNotExistError(self._name)

    def __str__(self) -> str:
        return self._stack.__str__()

    def __gather_vars__(self) -> int:
        """Helper method for calculating STATI extension vars."""
        max_init_vars_sum = 0
        for stack in self._stack:
            max_init_vars_sum += stack.MaxInitVars

        return max_init_vars_sum


class LabelFrame(FrameBase):
    """Label Frame class that represents label Frame."""

    def __init__(self):
        super().__init__("Label")
        self.init()

    def get(self, item: Argument):
        try:
            super().get(item)
        except VarDoesNotExistsExc:
            raise LabDoesNotExistsExc(item.value)
        return self._dict[item.value]

    def add(self, label, order: int):
        dict_label_order = self._dict.get(label)
        if dict_label_order is None:
            self._dict[label] = order
        elif dict_label_order == order:
            self._dict[label] = order
        else:
            raise Redefinition(f"{label} at {order}")


class Stack(list):
    """Stack class representing ordinary stack."""

    def __init__(self, name) -> None:
        super().__init__()
        self._name = name

    def popitem(self):
        if len(self) == 0:
            raise MissingValue(self._name)

        item = self[(len(self) - 1)]
        self.pop()
        return item
