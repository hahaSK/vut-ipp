from IPPInter.Instructions.Instruction import TSymSymBase, Argument
from IPPInter.InterepretCustomExceptions import WrongOperandsType, StringOperationError

"""String operation instructions"""


class Concat(TSymSymBase):
    opCode = "CONCAT"

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type != Argument.type_string or sym2_type != Argument.type_string:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = sym1_val + sym2_val
        stacks[self.arg1.frame].assign(self.arg1, Argument.type_string, res_value)
        return super().do(stacks)


class StrLen(TSymSymBase):
    opCode = "STRLEN"

    def __init__(self, order: int, arg):
        super().__init__(order, arg, argc=2)

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        if sym1_type != Argument.type_string:
            raise WrongOperandsType(f" {self.opCode} {self.order}")

        res_value = len(sym1_val)
        stacks[self.arg1.frame].assign(self.arg1, Argument.type_int, res_value)
        return super().do(stacks)


class GetChar(TSymSymBase):
    opCode = "GETCHAR"

    def do(self, stacks):
        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type != Argument.type_string or sym2_type != Argument.type_int:
            raise WrongOperandsType(f" {self.opCode} {self.order}")
        if sym2_val not in range(0, len(sym1_val)):
            raise StringOperationError(f" {self.opCode} {self.order}")

        res_value = sym1_val[sym2_val]
        stacks[self.arg1.frame].assign(self.arg1, Argument.type_string, res_value)
        return super().do(stacks)


class SetChar(TSymSymBase):
    opCode = "SETCHAR"

    def do(self, stacks):
        res_type, res_val = stacks[self.arg1.frame].get(self.arg1)

        sym1_type, sym1_val = self.__get_operands__(stacks, self.arg2)
        sym2_type, sym2_val = self.__get_operands__(stacks, self.arg3)
        if sym1_type != Argument.type_int or sym2_type != Argument.type_string or res_type != Argument.type_string:
            raise WrongOperandsType(f" {self.opCode} {self.order}")
        if sym1_val not in range(0, len(res_val)) or len(sym2_val) == 0:
            raise StringOperationError(f" {self.opCode} {self.order}")

        res_val = list(res_val)
        res_val[sym1_val] = sym2_val[0]
        res_value = "".join(res_val)

        stacks[self.arg1.frame].assign(self.arg1, res_type, res_value)
        return super().do(stacks)
