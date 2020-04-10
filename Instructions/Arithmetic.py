from Instructions.Instruction import TSymSymBase, Argument
from InterepretCustomExceptions import WrongOperandsType, StringOperationError, BadValueError

"""Arithmetic operations"""


class Add(TSymSymBase):
    opCode = "ADD"

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type != Argument.type_int or sym2_type != Argument.type_int:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = sym1_val + sym2_val
        stacks[self.arg1.frame].assign(self.arg1, Argument.type_int, res_value)

        return super().do(stacks)


class Sub(TSymSymBase):
    opCode = "SUB"

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type != Argument.type_int or sym2_type != Argument.type_int:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = sym1_val - sym2_val
        stacks[self.arg1.frame].assign(self.arg1, Argument.type_int, res_value)

        return super().do(stacks)


class Mul(TSymSymBase):
    opCode = "MUL"

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type != Argument.type_int or sym2_type != Argument.type_int:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = sym1_val * sym2_val
        stacks[self.arg1.frame].assign(self.arg1, Argument.type_int, res_value)

        return super().do(stacks)


class IDiv(TSymSymBase):
    opCode = "IDIV"

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type != Argument.type_int or sym2_type != Argument.type_int:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        if sym2_val == 0:
            raise BadValueError(f" {self.opCode} {self.order}")

        res_value = sym1_val // sym2_val
        stacks[self.arg1.frame].assign(self.arg1, Argument.type_int, res_value)

        return super().do(stacks)


class LT(TSymSymBase):
    opCode = "LT"

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type != Argument.type_int or sym2_type != Argument.type_int:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = sym1_val < sym2_val
        stacks[self.arg1.frame].assign(self.arg1, Argument.type_int, res_value)

        return super().do(stacks)


class GT(TSymSymBase):
    opCode = "GT"

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type != sym2_type:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = sym1_val > sym2_val
        stacks[self.arg1.frame].assign(self.arg1, Argument.type_bool, res_value)

        return super().do(stacks)


class EQ(TSymSymBase):
    opCode = "EQ"

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type != sym2_type:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = sym1_val == sym2_val
        stacks[self.arg1.frame].assign(self.arg1, Argument.type_bool, res_value)

        return super().do(stacks)


class And(TSymSymBase):
    opCode = "AND"

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type != Argument.type_bool or sym2_type != Argument.type_bool:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = sym1_val and sym2_val
        stacks[self.arg1.frame].assign(self.arg1, Argument.type_bool, res_value)

        return super().do(stacks)


class Or(TSymSymBase):
    opCode = "OR"

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type != Argument.type_bool or sym2_type != Argument.type_bool:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = sym1_val or sym2_val
        stacks[self.arg1.frame].assign(self.arg1, Argument.type_bool, res_value)

        return super().do(stacks)


class Not(TSymSymBase):
    opCode = "NOT"

    def __init__(self, order: int, arg):
        super().__init__(order, arg, argc=2)

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        if sym1_type != Argument.type_bool:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = not sym1_val
        stacks[self.arg1.frame].assign(self.arg1, Argument.type_bool, res_value)

        return super().do(stacks)


class Int2Char(TSymSymBase):
    opCode = "INT2CHAR"

    def __init__(self, order: int, arg):
        super().__init__(order, arg, argc=2)

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        if sym1_type != Argument.type_int:
            WrongOperandsType(f" {self.opCode} {self.order}")

        try:
            res_value = chr(sym1_val)
        except ValueError:
            raise StringOperationError(f" {self.opCode} {self.order}")

        stacks[self.arg1.frame].assign(self.arg1, Argument.type_string, res_value)

        return super().do(stacks)


class Stri2Int(TSymSymBase):
    opCode = "STRI2INT"

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type != Argument.type_string or sym2_type != Argument.type_int:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        if sym2_val not in range(0, len(sym1_val)):
            raise StringOperationError(f" {self.opCode} {self.order}")

        try:
            res_value = ord(sym1_val[sym2_val])
        except:
            raise StringOperationError(f" {self.opCode} {self.order}")

        stacks[self.arg1.frame].assign(self.arg1, Argument.type_int, res_value)
        return super().do(stacks)