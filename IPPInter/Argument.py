import re
from IPPInter.InterpretPatterns import Patterns
from IPPInter.InterepretCustomExceptions import *


def __replace_esc_seq__(value: str):
    esc_seq_pattern = r"\\([\d+]{3})"
    matched = re.findall(esc_seq_pattern, value)
    if not matched:
        return value
    for match in matched:
        if int(match) not in range(0, 1000):
            raise ArgError("Escape sequence out of range")
        value = value.replace("\\" + match, chr(int(match)))

    return value


class Argument:
    _patterns = Patterns()

    Non_term_var = "var"
    Non_term_symbol = "symbol"
    Non_term_label = "label"
    Non_term_type = "type"

    type_int = "int"
    type_bool = "bool"
    type_string = "string"
    type_var = "var"
    type_nil = "nil"
    _types = [type_int, type_bool, type_string, type_var, type_nil]

    @property
    def i_type(self):
        return self._type

    @i_type.setter
    def i_type(self, value):
        if value not in self._types:
            raise AttributeError("Type " + value + " not found")
        self._type = value

    @property
    def frame(self):
        return self._frame

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    def __init__(self):
        self._type = None
        self._frame = None
        self._value = None

    def set(self, arg, non_term):
        arg_type = arg.get("type")
        try:
            if not re.match(getattr(self._patterns, non_term + "_type"), arg_type):
                raise ArgError("Argument type mismatch. Expected type" + non_term + "_type")
        except AttributeError:
            raise ArgError(f"Type pattern for type {non_term} not implemented")

        re_opt = 0
        if re.match(getattr(self._patterns, "const_type"), arg_type):
            re_opt = re.IGNORECASE

        if arg_type == self.type_string and arg.text is None:
            arg.text = ''

        try:
            if not re.match(getattr(self._patterns, non_term + "_val"), arg.text, flags=re_opt):
                raise ArgError("Argument value mismatch. Expected regex " + getattr(self._patterns, non_term + "_val"))
        except AttributeError:
            raise ArgError(f"Value pattern for type {non_term} not implemented")

        self._value = arg.text
        self._frame = None
        if arg_type == self.Non_term_var:
            self._frame, self._value = arg.text.split('@')

        if arg_type != self.Non_term_label and arg_type != self.Non_term_type:
            self._value = self.__convert_type_to_py_type__(arg_type, self._value)
        self._type = arg_type

    def __convert_type_to_py_type__(self, arg_type, value):
        if arg_type == self.Non_term_var:
            return value
        if arg_type == self.type_int:
            try:
                return int(value)
            except ValueError:
                raise ArgError("Argument value mismatch. Expected int, got: " + str(value))
        if arg_type == self.type_bool:
            if value.lower() == "true":
                return True
            else:
                return False
        if arg_type == self.type_nil:
            return None
        if arg_type == self.type_string:
            return __replace_esc_seq__(value)
        else:
            raise InternalError("Type not implemented in converter")
