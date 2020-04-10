import sys

from Instructions.ProgramFlow import Label
from InterpretReturnCodes import ErrorPrints

from XMLParser import XMLParser
from Frame import Frame, LabelFrame, Stack, LocalFrame
from InterepretCustomExceptions import IPPBaseException


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def redirect_stdin(file):
    if file != "stdin":
        sys.stdin = open(file, "r")


class IPPInterpret(metaclass=Singleton):
    Stacks = {
        "GF": Frame("GF"),
        "LF": LocalFrame(),
        "TF": Frame("TF"),
        "CallStc": Stack("Call stack"),
        "Data": Stack("Data stack"),
        "label": LabelFrame()
    }

    _inst_count = 0
    _old_stdin = sys.stdin

    @property
    def inst_count(self):
        return IPPInterpret._inst_count

    def __init__(self) -> None:
        self.Stacks["GF"].init()
        self.Stacks["LF"].init()
        super().__init__()

    def interpret(self, files):
        redirect_stdin(files["input"])
        xml_instr = XMLParser().parse(files["source"])
        inst = ''
        try:
            for inst in xml_instr:
                if isinstance(inst, Label):
                    inst.do(self.Stacks)
        except IPPBaseException as ex:
            ErrorPrints.interpret_err(f"{ex.message} in {inst.opCode} at {inst.order}", ex.ExitCode)

        try:
            for inst in xml_instr:
                jump, order = inst.do(self.Stacks)

                jump, return_jump = jump
                if jump:
                    xml_instr.jump_to_inst(order)
                    if return_jump:
                        xml_instr.skip()

                IPPInterpret._inst_count += 1
        except IPPBaseException as ex:
            ErrorPrints.interpret_err(f"{ex.message} in {inst.opCode} at {inst.order}", ex.ExitCode)

        finally:
            sys.stdin.close()
            sys.stdin = self._old_stdin
