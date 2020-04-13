"""
    VUT FIT IPP 2019/2020 project.
    Author: Ing. Juraj Lahvička
    2020
"""

import sys


def errprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class ErrorPrints:
    """Error print class that handles error printing"""

    @staticmethod
    def err_parameter():
        errprint("Parameter error.")
        sys.exit(10)

    @staticmethod
    def err_xml_not_well_formed():
        errprint("XML not well-formed.")
        sys.exit(31)

    @staticmethod
    def err_xml_structure(additional_msg):
        errprint("Unexpected XML structure. " + additional_msg)
        sys.exit(32)

    @staticmethod
    def file_error(msg):
        errprint(msg)
        sys.exit(11)

    @staticmethod
    def interpret_err(msg: str, exit_code: int):
        errprint(msg)
        sys.exit(exit_code)
