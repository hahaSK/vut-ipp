"""
    VUT FIT IPP 2019/2020 project.
    Author: Ing. Juraj Lahvička
    2020
"""

import sys

from IPPInter.Instructions.Instruction import BaseInstruction, Argument


class DPrint(BaseInstruction):
    opCode = "DPRINT"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order
        self.__check_sort_set_arg__(arg, 1)

    def __set_arg__(self, arg):
        self.arg1.set(arg[0], Argument.Non_term_symbol)

    def do(self, stacks):
        i_type, val = (self.arg1.i_type, self.arg1.value)
        if self.arg1.i_type == Argument.type_var:
            i_type, val = stacks[self.arg1.frame].get(self.arg1)

        print(val, file=sys.stderr)
        return super().do(stacks)


class Break(BaseInstruction):
    opCode = "BREAK"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order

    def __set_arg__(self, arg):
        pass

    def do(self, stacks):
        for stack, val in stacks.items():
            print(stack, file=sys.stderr, end=' ')
            print(val, file=sys.stderr, end='\n')

        from IPPInter.IPPInterpret import IPPInterpret
        print("Instruction count: " + str(IPPInterpret().inst_count), file=sys.stderr)

        return super().do(stacks)
