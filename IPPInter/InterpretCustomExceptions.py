"""
    VUT FIT IPP 2019/2020 project.
    Author: Ing. Juraj Lahvička
    2020
"""


class IPPBaseException(Exception):
    ExitCode = 1

    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = ''
        super().__init__(*args)


class ArgError(IPPBaseException):
    pass


class ParameterError(IPPBaseException):
    ExitCode = 10

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Parameter Error. " + self.message


class OpCodeError(IPPBaseException):
    ExitCode = 32

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "OpCode Error. " + self.message


class InternalError(IPPBaseException):
    ExitCode = 99

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Internal Error. " + self.message


class WrongOperandsType(IPPBaseException):
    ExitCode = 53

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Wrong operand types. " + self.message


class StringOperationError(IPPBaseException):
    ExitCode = 58

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "String operation error. " + self.message


class BadValueError(IPPBaseException):
    ExitCode = 57

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Bad value Error. " + self.message


class FrameDoesNotExistError(IPPBaseException):
    ExitCode = 55

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Frame does not exist. " + self.message


class VarDoesNotExistsExc(IPPBaseException):
    ExitCode = 54

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Variable does not exist. " + self.message


class LabDoesNotExistsExc(IPPBaseException):
    ExitCode = 52

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Label does not exist. " + self.message


class Redefinition(IPPBaseException):
    ExitCode = 52

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Redefinition. " + self.message


class MissingValue(IPPBaseException):
    ExitCode = 56

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = "Missing value. " + self.message
