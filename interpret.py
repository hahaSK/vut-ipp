"""
    VUT FIT IPP 2019/2020 project.
    Author: Ing. Juraj Lahvička
    2020
"""

import getopt
import sys

from IPPInter.IPPInterpret import IPPInterpret
from IPPInter.ErrorPrints import ErrorPrints, errprint


def print_help():
    """Prints help message."""
    print("Script interpret.py does interpretation of IPPcode20 from XML file.\n"
          "Usage: python interpret.py [--help|-h] [--source=file] [--input=file] [--stats=file] [--vars]* [--insts]*\n"
          "--help|-h    prints help to stdout.\n"
          "--source     path to XML file. If not set it reads from stdin.\n"
          "--input      path to file, from which the read instruction read. If not set it reads from stdin.\n"
          "--stats      path to file, where statistics will be written\n"
          "--vars       statistic option - max number of initialized variables\n"
          "--insts      statistic option - number of conducted instructions.\n"
          "at-least either --input or --source must be set")


def main(argv):
    _inputOpt = "input"
    _sourceOpt = "source"
    _stdin = "stdin"

    _statsOpt = "stats"
    _stats_extension = [_statsOpt + '=', "insts", "vars"]

    optlist = list()
    try:
        optlist, args = getopt.getopt(argv, "h", [_inputOpt + '=', _sourceOpt + '=', "help"] + _stats_extension)
    except getopt.GetoptError as e:
        errprint(e.msg)
        print_help()
        ErrorPrints.err_parameter()

    _optDic = {_inputOpt: _stdin, _sourceOpt: _stdin, "statOpt": list()}
    stats_set = False
    # Create option dictionary from passed arguments
    for opt, arg in optlist:
        if opt == "--help" or opt == "-h":
            print_help()
            sys.exit(0)
        elif opt in ("--" + _inputOpt, "--" + _sourceOpt):
            if arg != '':
                _optDic[str(opt).replace("--", '')] = arg
        elif opt == "--" + _statsOpt:
            stats_set = True
            _optDic[str(opt).replace("--", '')] = arg
        elif opt == "--insts" or opt == "--vars":
            _optDic["statOpt"] += [str(opt).replace("--", '')]

    # Check if at-least one of the parameters is set
    if _optDic[_inputOpt] == _stdin and _optDic[_sourceOpt] == _stdin:
        print_help()
        ErrorPrints.err_parameter()

    # For STATI extension the --stats= parameter must be set if other STATI parameters are set
    if not stats_set and len(_optDic["statOpt"]) != 0:
        print_help()
        ErrorPrints.err_parameter()

    # Run the interpret
    IPPInterpret().interpret(_optDic)


if __name__ == "__main__":
    main(sys.argv[1:])
    sys.exit(0)
