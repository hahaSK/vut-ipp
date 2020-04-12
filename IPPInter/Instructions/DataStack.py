from abc import ABC

from IPPInter.Instructions.Instruction import BaseInstruction, Argument, TSymSymBase
from IPPInter.InterepretCustomExceptions import WrongOperandsType, StringOperationError

"""Data stack operations"""


class StackBase(BaseInstruction, ABC):

    def __init__(self, order: int, arg):
        super().__init__()
        self.order = order

    def set_arg(self, arg):
        pass


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


class ClearS(StackBase):
    opCode = "CLEARS"

    def do(self, stacks):
        stacks["Data"].clear()
        return super().do(stacks)


class AddS(StackBase):
    opCode = "ADDS"

    def do(self, stacks):
        sym2_type, sym2_val = stacks["Data"].pop()
        sym1_type, sym1_val = stacks["Data"].pop()

        self.__check_operand_types__(sym1_type, sym2_type, [Argument.type_int, Argument.type_float])

        res_value = sym1_val + sym2_val

        res_type = Argument.type_int
        if sym1_type == Argument.type_float and sym2_type == Argument.type_float:
            res_type = Argument.type_float

        stacks["Data"].append((res_type, res_value))
        return super().do(stacks)


class SubS(StackBase):
    opCode = "SUBS"

    def do(self, stacks):
        sym2_type, sym2_val = stacks["Data"].pop()
        sym1_type, sym1_val = stacks["Data"].pop()

        self.__check_operand_types__(sym1_type, sym2_type, [Argument.type_int, Argument.type_float])

        res_value = sym1_val - sym2_val

        res_type = Argument.type_int
        if sym1_type == Argument.type_float and sym2_type == Argument.type_float:
            res_type = Argument.type_float

        stacks["Data"].append((res_type, res_value))
        return super().do(stacks)


class MulS(StackBase):
    opCode = "MULS"

    def do(self, stacks):
        sym2_type, sym2_val = stacks["Data"].pop()
        sym1_type, sym1_val = stacks["Data"].pop()

        self.__check_operand_types__(sym1_type, sym2_type, [Argument.type_int, Argument.type_float])

        res_value = sym1_val * sym2_val

        res_type = Argument.type_int
        if sym1_type == Argument.type_float and sym2_type == Argument.type_float:
            res_type = Argument.type_float

        stacks["Data"].append((res_type, res_value))
        return super().do(stacks)


class IDivS(StackBase):
    opCode = "IDIVS"

    def do(self, stacks):
        sym2_type, sym2_val = stacks["Data"].pop()
        sym1_type, sym1_val = stacks["Data"].pop()

        self.__check_operand_types__(sym1_type, sym2_type, [Argument.type_int])

        res_value = sym1_val // sym2_val

        res_type = Argument.type_int

        stacks["Data"].append((res_type, res_value))
        return super().do(stacks)


class DivS(StackBase):
    opCode = "DIVS"

    def do(self, stacks):
        sym2_type, sym2_val = stacks["Data"].pop()
        sym1_type, sym1_val = stacks["Data"].pop()

        self.__check_operand_types__(sym1_type, sym2_type, [Argument.type_int, Argument.type_float])

        res_value = sym1_val / sym2_val

        res_type = Argument.type_int
        if sym1_type == Argument.type_float and sym2_type == Argument.type_float:
            res_type = Argument.type_float

        stacks["Data"].append((res_type, res_value))
        return super().do(stacks)


class LTS(StackBase):
    opCode = "LTS"

    def do(self, stacks):
        sym2_type, sym2_val = stacks["Data"].pop()
        sym1_type, sym1_val = stacks["Data"].pop()
        if sym1_type != sym2_type or sym1_type == Argument.type_nil or sym2_type == Argument.type_nil:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = sym1_val < sym2_val

        stacks["Data"].append((Argument.type_bool, res_value))
        return super().do(stacks)


class GTS(StackBase):
    opCode = "GTS"

    def do(self, stacks):
        sym2_type, sym2_val = stacks["Data"].pop()
        sym1_type, sym1_val = stacks["Data"].pop()
        if sym1_type != sym2_type or sym1_type == Argument.type_nil or sym2_type == Argument.type_nil:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = sym1_val > sym2_val

        stacks["Data"].append((Argument.type_bool, res_value))
        return super().do(stacks)


class EQS(StackBase):
    opCode = "EQS"

    def do(self, stacks):
        sym2_type, sym2_val = stacks["Data"].pop()
        sym1_type, sym1_val = stacks["Data"].pop()
        if sym1_type == Argument.type_nil or sym2_type == Argument.type_nil:
            pass
        elif sym1_type != sym2_type:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = sym1_val == sym2_val

        stacks["Data"].append((Argument.type_bool, res_value))
        return super().do(stacks)


class AndS(StackBase):
    opCode = "ANDS"

    def do(self, stacks):
        sym2_type, sym2_val = stacks["Data"].pop()
        sym1_type, sym1_val = stacks["Data"].pop()
        self.__check_operand_types__(sym1_type, sym2_type, [Argument.type_bool])

        res_value = sym1_val and sym2_val

        stacks["Data"].append((Argument.type_bool, res_value))
        return super().do(stacks)


class OrS(StackBase):
    opCode = "ORS"

    def do(self, stacks):
        sym2_type, sym2_val = stacks["Data"].pop()
        sym1_type, sym1_val = stacks["Data"].pop()
        self.__check_operand_types__(sym1_type, sym2_type, [Argument.type_bool])

        res_value = sym1_val or sym2_val

        stacks["Data"].append((Argument.type_bool, res_value))
        return super().do(stacks)


class NotS(StackBase):
    opCode = "NOTS"

    def do(self, stacks):
        sym1_type, sym1_val = stacks["Data"].pop()
        self.__check_operand_types__(sym1_type, None, [Argument.type_bool])

        res_value = not sym1_val

        stacks["Data"].append((Argument.type_bool, res_value))
        return super().do(stacks)


class Int2CharS(StackBase):
    opCode = "INT2CHARS"

    def do(self, stacks):
        sym1_type, sym1_val = stacks["Data"].pop()
        self.__check_operand_types__(sym1_type, None, [Argument.type_int])

        try:
            res_value = chr(sym1_val)
        except ValueError:
            raise StringOperationError(f" {self.opCode} {self.order}")

        stacks["Data"].append((Argument.type_string, res_value))
        return super().do(stacks)


class Int2FloatS(StackBase):
    opCode = "INT2FLOATS"

    def do(self, stacks):
        sym1_type, sym1_val = stacks["Data"].pop()

        self.__check_operand_types__(sym1_type, None, [Argument.type_int])

        try:
            res_value = float(sym1_val)
        except ValueError:
            raise StringOperationError(f" {self.opCode} {self.order}")

        stacks["Data"].append((Argument.type_float, res_value))
        return super().do(stacks)


class Float2IntS(StackBase):
    opCode = "FLOAT2INTS"

    def do(self, stacks):
        sym1_type, sym1_val = stacks["Data"].pop()

        self.__check_operand_types__(sym1_type, None, [Argument.type_float])

        try:
            res_value = int(sym1_val)
        except ValueError:
            raise StringOperationError(f" {self.opCode} {self.order}")

        stacks["Data"].append((Argument.type_int, res_value))
        return super().do(stacks)


class Stri2IntS(StackBase):
    opCode = "STRI2INTS"

    def do(self, stacks):
        sym2_type, sym2_val = stacks["Data"].pop()
        sym1_type, sym1_val = stacks["Data"].pop()

        self.__check_operand_types__(sym1_type, None, [Argument.type_string])
        self.__check_operand_types__(sym2_type, None, [Argument.type_int])

        if sym2_val not in range(0, len(sym1_val)):
            raise StringOperationError(f" {self.opCode} {self.order}")

        try:
            res_value = ord(sym1_val[sym2_val])
        except:
            raise StringOperationError(f" {self.opCode} {self.order}")

        stacks["Data"].append((Argument.type_int, res_value))
        return super().do(stacks)


class JumpIfEqS(TSymSymBase):
    opCode = "JUMPIFEQS"

    def __init__(self, order: int, arg):
        super().__init__(order, arg, Argument.Non_term_label, argc=1)

    def do(self, stacks):
        sym2_type, sym2_val = stacks["Data"].pop()
        sym1_type, sym1_val = stacks["Data"].pop()
        if sym1_type == sym2_type or sym1_type == Argument.type_nil or sym2_type == Argument.type_nil:
            pass
        else:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        return (sym1_val == sym2_val, False), stacks["label"].get(self.arg1)


class JumpIfNEqS(TSymSymBase):
    opCode = "JUMPIFNEQS"

    def __init__(self, order: int, arg):
        super().__init__(order, arg, Argument.Non_term_label, argc=1)

    def do(self, stacks):
        sym2_type, sym2_val = stacks["Data"].pop()
        sym1_type, sym1_val = stacks["Data"].pop()
        if sym1_type == sym2_type or sym1_type == Argument.type_nil or sym2_type == Argument.type_nil:
            pass
        else:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        return (sym1_val != sym2_val, False), stacks["label"].get(self.arg1)
