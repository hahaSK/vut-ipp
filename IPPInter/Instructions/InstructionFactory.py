"""
    VUT FIT IPP 2019/2020 project.
    Author: Ing. Juraj Lahvička
    2020
"""

from IPPInter.InterpretCustomExceptions import OpCodeError

from IPPInter.Instructions.Arithmetic import Add, Sub, Mul, IDiv, LT, GT, EQ, And, Or, Not, Int2Char, Stri2Int, Div, \
    Float2Int, Int2Float
from IPPInter.Instructions.DataStack import Pushs, Pops, ClearS, AddS, SubS, MulS, IDivS, DivS, LTS, GTS, EQS, AndS, \
    OrS, NotS, Int2CharS, Stri2IntS, Int2FloatS, Float2IntS, JumpIfEqS, JumpIfNEqS
from IPPInter.Instructions.Debug import DPrint, Break
from IPPInter.Instructions.FrameFunc import Move, CreateFrame, PushFrame, PopFrame, DefVar, Call, Return
from IPPInter.Instructions.IO import Read, Write
from IPPInter.Instructions.ProgramFlow import Label, Jump, JumpIfEq, JumpIfNEq, Exit
from IPPInter.Instructions.String import Concat, StrLen, GetChar, SetChar
from IPPInter.Instructions.Type import Type


def instruction_factory(op_code, order: int, arg):
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
    elif op_code.upper() == Div.opCode:
        return Div(order, arg)
    elif op_code.upper() == Float2Int.opCode:
        return Float2Int(order, arg)
    elif op_code.upper() == Int2Float.opCode:
        return Int2Float(order, arg)
    # Data stack
    elif op_code.upper() == Pushs.opCode:
        return Pushs(order, arg)
    elif op_code.upper() == Pops.opCode:
        return Pops(order, arg)
    elif op_code.upper() == ClearS.opCode:
        return ClearS(order, arg)
    elif op_code.upper() == AddS.opCode:
        return AddS(order, arg)
    elif op_code.upper() == SubS.opCode:
        return SubS(order, arg)
    elif op_code.upper() == MulS.opCode:
        return MulS(order, arg)
    elif op_code.upper() == IDivS.opCode:
        return IDivS(order, arg)
    elif op_code.upper() == DivS.opCode:
        return DivS(order, arg)
    elif op_code.upper() == LTS.opCode:
        return LTS(order, arg)
    elif op_code.upper() == GTS.opCode:
        return GTS(order, arg)
    elif op_code.upper() == EQS.opCode:
        return EQS(order, arg)
    elif op_code.upper() == AndS.opCode:
        return AndS(order, arg)
    elif op_code.upper() == OrS.opCode:
        return OrS(order, arg)
    elif op_code.upper() == NotS.opCode:
        return NotS(order, arg)
    elif op_code.upper() == Int2CharS.opCode:
        return Int2CharS(order, arg)
    elif op_code.upper() == Stri2IntS.opCode:
        return Stri2IntS(order, arg)
    elif op_code.upper() == Int2FloatS.opCode:
        return Int2FloatS(order, arg)
    elif op_code.upper() == Float2IntS.opCode:
        return Float2IntS(order, arg)
    elif op_code.upper() == JumpIfEqS.opCode:
        return JumpIfEqS(order, arg)
    elif op_code.upper() == JumpIfNEqS.opCode:
        return JumpIfNEqS(order, arg)
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
