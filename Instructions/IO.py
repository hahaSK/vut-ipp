from Instructions.Instruction import BaseInstruction, Argument, ArgError
from InterepretCustomExceptions import InternalError

"""Input/Output instructions"""


class Read(BaseInstruction):
    opCode = "READ"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order
        self.__check_sort_set_arg__(arg, 2)

    def set_arg(self, arg):
        self.arg1.set(arg[0], Argument.Non_term_var)
        self.arg2.set(arg[1], Argument.Non_term_type)

    def do(self, stacks):
        try:
            val = input()
        except:
            val = ''

        try:
            self.arg2.set(type('', (object,), {"get": (lambda key: {"type": self.arg2.value}[key]), "text": val}),
                          self.arg2.value)
        except ArgError:
            self.arg2.i_type = Argument.type_nil
            self.arg2.value = None
        except InternalError:
            self.arg2.i_type = Argument.type_nil
            self.arg2.value = None

        stacks[self.arg1.frame].assign(self.arg1, self.arg2.i_type, self.arg2.value)

        return super().do(stacks)


class Write(BaseInstruction):
    opCode = "WRITE"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order
        self.__check_sort_set_arg__(arg, 1)

    def set_arg(self, arg):
        self.arg1.set(arg[0], Argument.Non_term_symbol)

    def do(self, stacks):
        i_type, val = (self.arg1.i_type, self.arg1.value)
        if self.arg1.i_type == Argument.type_var:
            i_type, val = stacks[self.arg1.frame].get(self.arg1)

        if i_type == Argument.type_bool:
            val = str(val).lower()
        if val is None:
            val = ''

        print(val, end='')

        return super().do(stacks)
