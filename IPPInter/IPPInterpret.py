"""
    VUT FIT IPP 2019/2020 project.
    Author: Ing. Juraj Lahvička
    2020
"""

import sys

from IPPInter.Instructions.ProgramFlow import Label
from IPPInter.ErrorPrints import ErrorPrints

from IPPInter.XMLParser import XMLParser
from IPPInter.Frame import Frame, LabelFrame, Stack, LocalFrame
from IPPInter.InterpretCustomExceptions import IPPBaseException


class Singleton(type):
    """Singleton metaclass."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def redirect_stdin(file):
    """If input is not supplied from stdin redirect the stdin to file."""
    if file != "stdin":
        try:
            sys.stdin = open(file, "r")
        except:
            ErrorPrints.file_error("Cannot open file for input")


class IPPInterpret(metaclass=Singleton):
    """Interpret singleton class."""
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

    # Instruction count property
    @property
    def inst_count(self):
        return IPPInterpret._inst_count

    def __init__(self) -> None:
        self.Stacks["GF"].init()
        self.Stacks["LF"].init()
        super().__init__()

    def interpret(self, options):
        xml_instr = XMLParser().parse(options["source"])
        redirect_stdin(options["input"])

        # First try to find all labels for the jumps
        inst = ''
        try:
            for inst in xml_instr:
                if isinstance(inst, Label):
                    inst.do(self.Stacks)
        except IPPBaseException as ex:
            ErrorPrints.interpret_err(f"{ex.message} in {inst.opCode} at {inst.order}", ex.ExitCode)

        # Execute each instruction
        try:
            for inst in xml_instr:
                IPPInterpret._inst_count += 1
                jump, order = inst.do(self.Stacks)

                # Unpack the jump tuple
                jump, return_jump = jump
                if jump:
                    # Jump to instruction
                    xml_instr.jump_to_inst(order)
                    # When the jump is from Return instruction we are jumping back to the Call instruction, so need to
                    # skip the call instruction
                    if return_jump:
                        xml_instr.skip()

        except IPPBaseException as ex:
            ErrorPrints.interpret_err(f"{ex.message} in {inst.opCode} at {inst.order}", ex.ExitCode)

        finally:
            sys.stdin.close()
            sys.stdin = self._old_stdin

        # Write statistics for the STATI extension
        if options.get("stats") is not None:
            write_stats(options, self.Stacks)


def write_stats(options, stacks):
    """Writes statistics to specified file"""
    try:
        file = open(options["stats"], "w")

        file_content = ''
        for option in options["statOpt"]:
            if option == "insts":
                file_content += f"{IPPInterpret().inst_count}\n"
            elif option == "vars":
                file_content += f"{stacks['GF'].MaxInitVars + stacks['LF'].MaxInitVars + stacks['TF'].MaxInitVars}\n"

        file.write(file_content)
        file.close()

    except OSError:
        ErrorPrints.file_error(f"Cannot open {options.get('stats')} file")
