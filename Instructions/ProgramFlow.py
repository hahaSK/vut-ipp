import sys
from abc import ABC

from Instructions.Instruction import TSymSymBase, Argument
from InterepretCustomExceptions import WrongOperandsType, BadValueError

"""Program flow instructions"""


class Label(TSymSymBase):
    opCode = "LABEL"

    def __init__(self, order: int, arg):
        super().__init__(order, arg, Argument.Non_term_label, argc=1)

    def set_arg(self, arg):
        self.arg1.set(arg[0], Argument.Non_term_label)

    def do(self, stacks):
        stacks["label"].add(self.arg1.value, self.order)
        return super().do(stacks)


class Jump(TSymSymBase):
    opCode = "JUMP"

    def __init__(self, order: int, arg):
        super().__init__(order, arg, Argument.Non_term_label, argc=1)

    def set_arg(self, arg):
        self.arg1.set(arg[0], Argument.Non_term_label)

    def do(self, stacks):
        return (True, False), stacks["label"].get(self.arg1)


class JumpIfEq(TSymSymBase):
    opCode = "JUMPIFEQ"

    def __init__(self, order: int, arg):
        super().__init__(order, arg, Argument.Non_term_label)

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type == sym2_type or sym1_type == Argument.type_nil or sym2_type == Argument.type_nil:
            pass
        else:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        return (sym1_val == sym2_val, False), stacks["label"].get(self.arg1)


class JumpIfNEq(TSymSymBase):
    opCode = "JUMPIFNEQ"

    def __init__(self, order: int, arg):
        super().__init__(order, arg, Argument.Non_term_label)

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type == sym2_type or sym1_type == Argument.type_nil or sym2_type == Argument.type_nil:
            pass
        else:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        return (sym1_val != sym2_val, False), stacks["label"].get(self.arg1)


class Exit(TSymSymBase):
    opCode = "EXIT"

    def __init__(self, order: int, arg):
        super().__init__(order, arg, Argument.Non_term_label, argc=1)

    def set_arg(self, arg):
        self.arg1.set(arg[0], Argument.Non_term_symbol)

    def do(self, stacks):
        i_type, val = (self.arg1.i_type, self.arg1.value)
        if self.arg1.i_type == Argument.type_var:
            i_type, val = stacks[self.arg1.frame].get(self.arg1)

        if i_type != Argument.type_int:
            raise WrongOperandsType(f" {self.opCode} {self.order}")
        if val not in range(0, 50):
            raise BadValueError(f" {self.opCode} {self.order}")

        sys.exit(val)
