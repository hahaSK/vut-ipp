import getopt
import sys

from IPPInter.IPPInterpret import IPPInterpret
from IPPInter.InterpretReturnCodes import ErrorPrints, errprint


def print_help():
    # TODO message
    print("help\n")


def main(argv):
    _inputOpt = "input"
    _sourceOpt = "source"
    _stdin = "stdin"

    optlist = list()
    try:
        optlist, args = getopt.getopt(argv, "h", [_inputOpt + '=', _sourceOpt + '=', "help"])
    except getopt.GetoptError as e:
        errprint(e.msg)
        print_help()
        ErrorPrints.err_parameter()

    _optDic = {_inputOpt: _stdin, _sourceOpt: _stdin}
    for opt, arg in optlist:
        if opt == "--help" or opt == "-h":
            print_help()
            sys.exit(0)
        elif opt in ("--" + _inputOpt, "--" + _sourceOpt):
            if arg != '':
                _optDic[str(opt).replace("--", '')] = arg

    if _optDic[_inputOpt] == _stdin and _optDic[_sourceOpt] == _stdin:
        print_help()
        ErrorPrints.err_parameter()

    IPPInterpret().interpret(_optDic)


if __name__ == "__main__":
    main(sys.argv[1:])
    sys.exit(0)
