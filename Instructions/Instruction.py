from abc import ABC, abstractmethod

from InterepretCustomExceptions import *
from Argument import Argument


class BaseInstruction(ABC):
    opCode = None

    @abstractmethod
    def __init__(self):
        self.order = 0
        self.arg1 = None
        self.arg2 = None
        self.arg3 = None

    def argc(self):
        count = 0
        if self.arg1 is not None:
            count += 1
        if self.arg2 is not None:
            count += 1
        if self.arg3 is not None:
            count += 1
        return count

    def __check_sort_set_arg__(self, arg, count):
        arg[:] = sorted(arg, key=lambda child: child.tag)
        try:
            if count == 1:
                self.arg1 = Argument()
            elif count == 2:
                self.arg1 = Argument()
                self.arg2 = Argument()
            elif count == 3:
                self.arg1 = Argument()
                self.arg2 = Argument()
                self.arg3 = Argument()
            else:
                raise InternalError(f" {self.opCode} {self.order}")
        except IndexError:
            raise ArgError(self.opCode + " order=" + str(self.order) + " has invalid arg count. Expected " + str(count))

        self.set_arg(arg)

    @abstractmethod
    def set_arg(self, arg):
        pass

    @abstractmethod
    def do(self, stacks):
        return (False, False), self.order


class TSymSymBase(BaseInstruction, ABC):
    def __init__(self, order: int, arg, non_term_first_arg=Argument.Non_term_var, argc=3):
        super().__init__()
        self.order = order
        self.first_type = non_term_first_arg
        self.__check_sort_set_arg__(arg, argc)

    def set_arg(self, arg):
        self.arg1.set(arg[0], self.first_type)
        if self.arg2 is not None:
            self.arg2.set(arg[1], Argument.Non_term_symbol)
        if self.arg3 is not None:
            self.arg3.set(arg[2], Argument.Non_term_symbol)

    def __get_operands__(self, stacks, arg: Argument):
        sym_type = sym_val = None
        if arg is not None:
            sym_type = arg.i_type
            sym_val = arg.value
            if arg.i_type == Argument.Non_term_var:
                sym_type, sym_val = stacks[arg.frame].get(arg)

        return sym_type, sym_val
