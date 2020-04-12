import sys

from IPPInter.Instructions.ProgramFlow import Label
from IPPInter.InterpretReturnCodes import ErrorPrints

from IPPInter.XMLParser import XMLParser
from IPPInter.Frame import Frame, LabelFrame, Stack, LocalFrame
from IPPInter.InterepretCustomExceptions import IPPBaseException


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def redirect_stdin(file):
    if file != "stdin":
        try:
            sys.stdin = open(file, "r")
        except:
            ErrorPrints.file_error("Cannot open file for input")


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

    def interpret(self, options):
        xml_instr = XMLParser().parse(options["source"])
        redirect_stdin(options["input"])
        inst = ''
        try:
            for inst in xml_instr:
                if isinstance(inst, Label):
                    inst.do(self.Stacks)
        except IPPBaseException as ex:
            ErrorPrints.interpret_err(f"{ex.message} in {inst.opCode} at {inst.order}", ex.ExitCode)

        try:
            for inst in xml_instr:
                IPPInterpret._inst_count += 1
                jump, order = inst.do(self.Stacks)

                jump, return_jump = jump
                if jump:
                    xml_instr.jump_to_inst(order)
                    if return_jump:
                        xml_instr.skip()

        except IPPBaseException as ex:
            ErrorPrints.interpret_err(f"{ex.message} in {inst.opCode} at {inst.order}", ex.ExitCode)

        finally:
            sys.stdin.close()
            sys.stdin = self._old_stdin

        if options.get("stats") is not None:
            write_stats(options, self.Stacks)


def write_stats(options, stacks):
    try:
        file = open(options["stats"], "w")

        file_content = ''
        for option in options["statOpt"]:
            if option == "insts":
                file_content += f"{IPPInterpret().inst_count}\n"
                # file.write(str(IPPInterpret().inst_count))
            elif option == "vars":
                file_content += f"{stacks['GF'].MaxInitVars + stacks['LF'].MaxInitVars + stacks['TF'].MaxInitVars}\n"
                # file.write(str(stacks["GF"].MaxInitVars + stacks["LF"].MaxInitVars + stacks["TF"].MaxInitVars))

        file.write(file_content)
        file.close()

    except OSError:
        ErrorPrints.file_error(f"Cannot open {options.get('stats')} file")
