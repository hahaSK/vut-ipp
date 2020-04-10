from Instructions.Instruction import BaseInstruction, Argument

"""Type operations"""


class Type(BaseInstruction):
    opCode = "TYPE"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order
        self.__check_sort_set_arg__(arg, 2)

    def set_arg(self, arg):
        self.arg1.set(arg[0], Argument.Non_term_var)
        self.arg2.set(arg[1], Argument.Non_term_symbol)

    def do(self, stacks):
        sym_type, sym_val = (self.arg2.i_type, self.arg2.value)
        if self.arg2.i_type == Argument.type_var:
            sym_type, sym_val = stacks[self.arg2.frame].get(self.arg2, False)

        if sym_val is None and self.arg2.i_type == Argument.type_var:
            sym_type = ''

        stacks[self.arg1.frame].assign(self.arg1, Argument.type_string, sym_type)

        return super().do(stacks)
