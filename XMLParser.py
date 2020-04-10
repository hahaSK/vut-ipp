import sys
import xml.etree.ElementTree as ET
from InterpretReturnCodes import ErrorPrints
from Instructions.InstructionFactory import InstructionFactory
from InterepretCustomExceptions import ArgError, OpCodeError
from InstructionsCollection import InstructionsCollection


class XMLParser:

    def parse(self, file):
        tree = ET.ElementTree
        try:
            if file == "stdin":
                tree = ET.parse(sys.stdin)
            else:
                tree = ET.parse(file)
        except FileNotFoundError:
            ErrorPrints.file_error(f"{file} not found")
        except:
            ErrorPrints.err_xml_not_well_formed()

        """ Get head """
        root = tree.getroot()
        self.__check_head__(root)

        inst = root.findall("instruction")
        if inst != root.getchildren():
            ErrorPrints.err_xml_structure("Unsupported element")

        try:
            inst[:] = sorted(inst, key=lambda child: int(child.get("order")))
        except:
            ErrorPrints.err_xml_structure("Invalid order attribute")

        self.__check_inst__(inst)

        if len(inst) != 0:
            if int(inst[0].attrib.get("order")) <= 0:
                ErrorPrints.err_xml_structure("Order must be positive number")

        return self.__create_instructions__(inst)

    def __check_head__(self, root):
        if len(root.attrib) < 1 or len(root.attrib) > 3:
            ErrorPrints.err_xml_structure("Wrong root element")

        if root.tag != "program":
            ErrorPrints.err_xml_structure("Wrong root element")

        lang = root.attrib.get("language")
        name = root.attrib.get("language")
        description = root.attrib.get("description")

        if lang is None:
            ErrorPrints.err_xml_structure("Wrong root element")
        if len(root.attrib) == 2 and name is None and description is None:
            ErrorPrints.err_xml_structure("Wrong root element")
        if len(root.attrib) == 3 and (name is None or description is None):
            ErrorPrints.err_xml_structure("Wrong root element")

    def __check_inst__(self, items):
        uniq = list()
        for item in items:
            self.__check_inst_attrib__(item)
            if item.attrib["order"] in uniq:
                ErrorPrints.err_xml_structure("Duplicity order number " + str(item.attrib["order"]))

            try:
                self.__check_inst_child__(item.getchildren())
            except ArgError as e:
                ErrorPrints.err_xml_structure(e.message + f"At item {item.attrib['order']}")

            uniq.append(item.attrib["order"])

    def __check_inst_attrib__(self, item):
        if item.get("order") is None or item.get("opcode") is None:
            ErrorPrints.err_xml_structure("Missing order or opcode attribute in " + str(item))
        if len(item.attrib) > 2:
            ErrorPrints.err_xml_structure(f"Unexpected attribute in {item['opcode']} at {item['order']}")

    def __check_inst_child__(self, arguments):
        if len(arguments) == 0:
            return

        arg1 = arg2 = arg3 = False
        for argument in arguments:
            if len(argument.getchildren()) != 0:
                raise ArgError("Unexpected nested element at " + str(argument))

            if len(argument.attrib) != 1:
                raise ArgError("Unexpected argument attribute. Expected attribute 'type'. " + str(argument.attrib))
            if argument.get("type") is None:
                raise ArgError("Argument attribute 'type' not found." + str(argument))

            arg1 = self.__check_arg__(arg1, argument, "arg1")
            arg2 = self.__check_arg__(arg2, argument, "arg2")
            arg3 = self.__check_arg__(arg3, argument, "arg3")

        if not arg1:
            raise ArgError("Unexpected argument element. Argument 1 not set")
        if not arg2 and (len(arguments) == 2 or len(arguments) == 3):
            raise ArgError("Unexpected argument element. Argument 2 not set")
        if not arg3 and len(arguments) == 3:
            raise ArgError("Unexpected argument element. Argument 3 not set")
        if len(arguments) > 3:
            raise ArgError("Unexpected argument element.")

    def __check_arg__(self, arg, argument, arg_name):
        if arg and argument.tag == arg_name:
            raise ArgError("Redefinition of " + arg_name)
        elif not arg and argument.tag == arg_name:
            arg = True

        return arg

    def __create_instructions__(self, instructions):
        __instructions = list()
        inst = []
        try:
            for inst in instructions:
                children = inst.getchildren()
                instruction = InstructionFactory.get_instruction(inst.attrib["opcode"], int(inst.attrib["order"]),
                                                                 children)

                if instruction.argc() != len(children):
                    ErrorPrints.err_xml_structure(f"Argument count at {inst.attrib['order']} {inst.attrib['opcode']}")

                __instructions.append(instruction)
        except ArgError as ex:
            ErrorPrints.err_xml_structure(ex.message + f" At {inst.get('order')} {inst.get('opcode')}")
        except OpCodeError as ex:
            ErrorPrints.err_xml_structure(ex.message + f" At {inst.get('order')} {inst.get('opcode')}")
        except IndexError as ex:
            msg = ex.args[0]
            ErrorPrints.err_xml_structure(msg + f" At {inst.get('order')} {inst.get('opcode')}")

        return InstructionsCollection(__instructions)
