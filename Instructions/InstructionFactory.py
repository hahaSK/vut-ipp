from InterepretCustomExceptions import OpCodeError

from Instructions.Arithmetic import Add, Sub, Mul, IDiv, LT, GT, EQ, And, Or, Not, Int2Char, Stri2Int
from Instructions.DataStack import Pushs, Pops
from Instructions.Debug import DPrint, Break
from Instructions.FrameFunc import Move, CreateFrame, PushFrame, PopFrame, DefVar, Call, Return
from Instructions.IO import Read, Write
from Instructions.ProgramFlow import Label, Jump, JumpIfEq, JumpIfNEq, Exit
from Instructions.String import Concat, StrLen, GetChar, SetChar
from Instructions.Type import Type


class InstructionFactory:
    @classmethod
    def get_instruction(cls, op_code, order: int, arg):
        """ Arithmetic """
        if op_code.upper() == Add.opCode:
            return Add(order, arg)
        elif op_code.upper() == Sub.opCode:
            return Sub(order, arg)
        elif op_code.upper() == Mul.opCode:
            return Mul(order, arg)
        elif op_code.upper() == IDiv.opCode:
            return IDiv(order, arg)
        elif op_code.upper() == LT.opCode:
            return LT(order, arg)
        elif op_code.upper() == GT.opCode:
            return GT(order, arg)
        elif op_code.upper() == EQ.opCode:
            return EQ(order, arg)
        elif op_code.upper() == And.opCode:
            return And(order, arg)
        elif op_code.upper() == Or.opCode:
            return Or(order, arg)
        elif op_code.upper() == Not.opCode:
            return Not(order, arg)
        elif op_code.upper() == Int2Char.opCode:
            return Int2Char(order, arg)
        elif op_code.upper() == Stri2Int.opCode:
            return Stri2Int(order, arg)
        # Data stack
        elif op_code.upper() == Pushs.opCode:
            return Pushs(order, arg)
        elif op_code.upper() == Pops.opCode:
            return Pops(order, arg)
        # Debug
        elif op_code.upper() == DPrint.opCode:
            return DPrint(order, arg)
        elif op_code.upper() == Break.opCode:
            return Break(order, arg)
        # Frame/function
        elif op_code.upper() == Move.opCode:
            return Move(order, arg)
        elif op_code.upper() == CreateFrame.opCode:
            return CreateFrame(order, arg)
        elif op_code.upper() == PushFrame.opCode:
            return PushFrame(order, arg)
        elif op_code.upper() == PopFrame.opCode:
            return PopFrame(order, arg)
        elif op_code.upper() == DefVar.opCode:
            return DefVar(order, arg)
        elif op_code.upper() == Call.opCode:
            return Call(order, arg)
        elif op_code.upper() == Return.opCode:
            return Return(order, arg)
        # IO
        elif op_code.upper() == Read.opCode:
            return Read(order, arg)
        elif op_code.upper() == Write.opCode:
            return Write(order, arg)
        # Program flow
        elif op_code.upper() == Label.opCode:
            return Label(order, arg)
        elif op_code.upper() == Jump.opCode:
            return Jump(order, arg)
        elif op_code.upper() == JumpIfEq.opCode:
            return JumpIfEq(order, arg)
        elif op_code.upper() == JumpIfNEq.opCode:
            return JumpIfNEq(order, arg)
        elif op_code.upper() == Exit.opCode:
            return Exit(order, arg)
        # String
        elif op_code.upper() == Concat.opCode:
            return Concat(order, arg)
        elif op_code.upper() == StrLen.opCode:
            return StrLen(order, arg)
        elif op_code.upper() == GetChar.opCode:
            return GetChar(order, arg)
        elif op_code.upper() == SetChar.opCode:
            return SetChar(order, arg)
        elif op_code.upper() == Type.opCode:
            return Type(order, arg)
        else:
            raise OpCodeError()
