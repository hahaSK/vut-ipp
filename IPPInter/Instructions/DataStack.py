from IPPInter.Instructions.Instruction import BaseInstruction, Argument

"""Data stack operations"""


class Pushs(BaseInstruction):
    opCode = "PUSHS"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order
        self.__check_sort_set_arg__(arg, 1)

    def set_arg(self, arg):
        self.arg1.set(arg[0], Argument.Non_term_symbol)

    def do(self, stacks):
        typ_val = (self.arg1.i_type, self.arg1.value)
        if self.arg1.i_type == Argument.type_var:
            typ_val = stacks[self.arg1.frame].get(self.arg1)

        stacks["Data"].append(typ_val)
        return super().do(stacks)


class Pops(BaseInstruction):
    opCode = "POPS"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order
        self.__check_sort_set_arg__(arg, 1)

    def set_arg(self, arg):
        self.arg1.set(arg[0], Argument.Non_term_var)

    def do(self, stacks):
        typ_val = stacks["Data"].popitem()
        stacks[self.arg1.frame].assign(self.arg1, *typ_val)
        return super().do(stacks)
