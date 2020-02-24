# Documentation of Project Implementation for IPP 2019/2020
* Name and surname: **Juraj Lahvička**
* Login: <b>xlahvi00</b>

## 1. Analysis of IPPcode20

The analysis of the IPPcode20 source code is located in `IPPCodeParser.php`. Source code is read from standard input line by line. Each line/instruction is tested by PCRE regular expressions. This regular expressions check lexical and syntactic analysis. Regular expressions check operation code name, number of operands and their types. 

## 2. XML generator

The XML operations are handled in `XMLGenerator.php` in `XMLGenerator` class. When instantiating the class a new DOM document is created. The class has one public function `AddInstruction` which handles adding elements and adding correct attributes to elements.

## 3. Input arguments

Arguments are handled by getopt library: <https://www.php.net/manual/en/function.getopt.php>. All possible options are defined `Options.php`.

## 4. Return codes and error printing

Exit or return codes are handled by `ReturnCodes` class located in `ReturnCodes.php`. General messages are then taken from `Messages.php` where they are defined.

## 5. STATP extension

if _--stats=file_ is supplied then statistics of the source code are gathered. At the end the statistics are stored/saved in specified _file_. Statistics have different optional arguments:
* _--loc_ - counts number of instructions.
* _--comments_ - counts number of comments.
* _--labels_ - counts number of **unique** labels.
* _--jumps_ - counts number of conditional and unconditional jumps. 
