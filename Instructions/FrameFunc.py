from Instructions.Instruction import BaseInstruction, Argument

""" Frame instructions """


class Move(BaseInstruction):
    opCode = "MOVE"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order
        self.__check_sort_set_arg__(arg, 2)

    def set_arg(self, arg):
        self.arg1.set(arg[0], Argument.Non_term_var)
        self.arg2.set(arg[1], Argument.Non_term_symbol)

    def do(self, stacks):
        sym = self.arg2.i_type, self.arg2.value
        if self.arg2 == Argument.type_var:
            sym = stacks[self.arg2.frame].get(self.arg2)

        stacks[self.arg1.frame].assign(self.arg1, *sym)
        return super().do(stacks)


class CreateFrame(BaseInstruction):
    opCode = "CREATEFRAME"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order

    def set_arg(self, arg):
        pass

    def do(self, stacks):
        stacks["TF"].init()
        return super().do(stacks)


class PushFrame(BaseInstruction):
    opCode = "PUSHFRAME"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order

    def set_arg(self, arg):
        pass

    def do(self, stacks):
        stacks["LF"].push(stacks["TF"])
        stacks["TF"].clear()
        return super().do(stacks)


class PopFrame(BaseInstruction):
    opCode = "POPFRAME"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order

    def set_arg(self, arg):
        pass

    def do(self, stacks):
        stacks["TF"].replace(stacks["LF"].pop())
        return super().do(stacks)


class DefVar(BaseInstruction):
    opCode = "DEFVAR"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order
        self.__check_sort_set_arg__(arg, 1)

    def set_arg(self, arg):
        self.arg1.set(arg[0], Argument.Non_term_var)

    def do(self, stacks):
        stacks[self.arg1.frame].add(self.arg1)
        return super().do(stacks)


class Call(BaseInstruction):
    opCode = "CALL"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order
        self.__check_sort_set_arg__(arg, 1)

    def set_arg(self, arg):
        self.arg1.set(arg[0], Argument.Non_term_label)

    def do(self, stacks):
        order = stacks["label"].get(self.arg1)
        stacks["CallStc"].append(self)
        return (True, False), order


class Return(BaseInstruction):
    opCode = "RETURN"

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order

    def set_arg(self, arg):
        pass

    def do(self, stacks):
        inst = stacks["CallStc"].popitem()
        return (True, True), inst.order
