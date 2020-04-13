"""
    VUT FIT IPP 2019/2020 project.
    Author: Ing. Juraj Lahvička
    2020
"""

from IPPInter.Instructions.Instruction import BaseInstruction


class InstructionsCollection(object):
    """Custom Instruction collection iterable class, with possibility to jump to specific instruction order."""

    def __init__(self, values: [BaseInstruction]):
        self.values = values
        self.location = 0

    def __iter__(self):
        self.location = 0
        return self

    def __next__(self):
        if self.location == len(self.values):
            raise StopIteration
        value = self.values[self.location]
        self.location += 1
        return value

    def jump_to_inst(self, order):
        for i, inst in enumerate(self.values):
            if inst.order == order:
                self.location = i
                return

    def skip(self):
        self.__next__()
