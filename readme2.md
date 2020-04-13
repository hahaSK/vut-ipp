# Documentation of Project Implementation for IPP 2019/2020

* Name and surname: **Juraj Lahvička**
* Login: **xlahvi00**

# Interpret

## How to run

`python interpret.py [--help|-h] [--source=file] [--input=file] [--stats=file] [--vars] [--insts]`

* `--help|-h`       - prints help message.
* `--source=file`   - file to read XML from. If not supplied the XML is read from _stdin_.
* `--input=file`    - file to read input from. If not supplied the input is read from _stdin_. This options is only for _INPUT_ instruction. 
* `--stats=file`    - file to write the statistics into. 
* `--vars`          - max number of initialized variables in all frames.
* `--insts`         - number of instructions executed.

At least one of `--source=file` or `--input=file` parameter must be supplied.
When using `--vars` or `--insts` the `--stats=file` must be supplied.

## [interpret.py](interpret.py)

`interpret.py` is the main script for IPP interpret. It has the `main` function which checks the validity of parameters and their variance validity. When parameters are valid an option dictionary is created. Next the `IPPInterpret` class instance is created, on this instance, the option dictionary is passed to `interpret` method as argument. 

## [IPPInterpret](IPPInter/IPPInterpret.py)

`IPPInterpret` class is singleton (only one instance of this class is created). It contains dictionary of stacks (Global Frame, Local Frame, Temporary Frame, Call Stack, Data Stack, Label Stack), property of instruction count, and `interpret` method which takes one parameter `options`, which is supposed to by collection of options. 
At first the `XMLParser` class instance is created and its method `parse` is called, where `--source` option is supplied. This method returns custom instruction collection. Next the `--input` option is processed (the input is redirected to either _stdin_ or supplied _file_). After the redirection all the label instructions are executed. 
Reason for gathering all labels at the beginning is that when we reach some jump instruction to label, we don't have to look for the label. Executing each instruction is next. It is done by iterating over the custom instruction collection and calling its `do` method. This method returns `Jump` `tuple` and `order`, 
explanation of this will be in `BaseInstruction` class. After `do` method follows jump check. If jump is set the `jump_to_inst` method of the `InstructionsCollection` class is called, which handles jump to appropriate instruction. If jump is set by _RETURN_ instruction the instruction we jump to (instruction from Call Stack) is skipped,
because it is _CALL_ instruction and we don't want to execute the same _CALL_ instruction again (it would trigger infinite loop). 

These two iterations are wrapped in `try:` `except:` block to catch exceptions. As last thing, the statistics are written to specified file, which depends if `--stats=file` option is set.  

## [XMLParser](IPPInter/XMLParser.py)

`XMLParse` does parsing of the XML file, checking the correct format, checking the supported attributes, order uniqueness and also orders the instructions by order. If the XML is valid the parser moves to creation individual instructions from the XML (which are appended to the list of instructions), by calling the `InstructionFactory` class method `get_instrucion`. 
After it succeeds it returns the `InstructionsCollection` instance. The XMLParse does quite a lot of XML checks, which are not described here. For more info see [XMLParser.py](IPPInter/XMLParser.py).

## [Patterns](IPPInter/InterpretPatterns.py)

`Patterns` consists of only properties (getters only), that hold regex patterns for different non terminals, types and their values regex. For more info see [Patterns](IPPInter/InterpretPatterns.py).  

## [Argument](IPPInter/Argument.py)

`Argument` class represents instruction arguments. Class consists of fields:
 * `Patterns` class instance
 * Non terminal symbols
 * supported type text strings
 * types list
 
and properties:
 * i_type - type of the argument (getter and setter. Setter also checks for type that is being set to.)
 * frame - frame of the argument, if constant then the frame is `None`. (getter only) 
 * value - value of the argument (getter and setter)

The class has method `set` which takes 2 parameters. First is arg object from the XML and second is the non terminal symbol which should be set to. The non terminal symbol is used to get according patterns from `Patterns` instance, which are then used in `re` module for regex search. This method parses, checks and sets its fields/attributes from arg and converts value
to python value type. If some regex match is not valid, the `ArgError` exception is raised. 

## [ErrorPrints](IPPInter/ErrorPrints.py)

`ErrorPrints` class handles error printing to _stderr_ and exiting with specific exit code. This class can be considered as static. It has few predefined error methods and one "generic" method that takes 2 parameters: `msg` and `exit_code`.

## [Frame](IPPInter/Frame.py)

[Frame.py](IPPInter/Frame.py) file consist of several classes: 
1. `FrameBase` class is abstract base Frame class, which has a private dictionary field `_dict`, where variables are stored. Variables are stored in format: ```{'var_name`: ('var_type', var_value)}```. Method `init` creates new variable dictionary. Method `clear` sets the `_dict` field to `None`.
`get` is an abstract method which returns value, from the private `_dict` field, which is a tuple `('var_type', var_value)`. First the method calls another private method `__check_stack_init__` that performs check if the stack is initialized and after that another private method `__check_existence__`
that checks if the variable is in the dictionary. This method is marked as abstract. 
1. `Frame` class is used for GF and TF. It inherits from `FrameBase` so above mentioned text applies also to this class. It has field `MaxInitVars`, which is used in STATI extension. This class has `get` method, that takes 2 parameters, `item` which is and `Argument` class and other optional `check_init` which is by default set to `True`.
This method at first call `super().get` method to do the above mentioned checks and after that does calls private `__check_var_init__` method to check if the variable is initialized. This check is only done if the `check_init` parameter is set to `True`. `Assign` method takes 3 parameters: `to` `Argument` class 
instance to assign to (this doesn't change anything on the `Argument` class instance, it only uses it to search the variable in the dictionary) `other_type` and `other_value`. It does stack init and variable existence checks and than adds tuple `(other_type, other_value)` to the `to.value` variable. `add` method does again the stack init check and 
variable redefinition check. After that it creates new variable in the `_dict`, which is uninitialized. Last is `replace`, which takes 1 parameter: `other` which is a `Frame` class instance and replaces self `_dict` with other `_dict` field.
1. `LocalFrame` this class is basically just list of `Frame` classes and points to the top Frame on the list. Almost all of the methods has the same functionality sa `Frame` class. For more info see [LocalFrame](IPPInter/Frame.py).
1. `LabelFrame` inherits from `FrameBase`. it is basically an dictionary of labels, which looks like this: ```{'label_name`: order}```, where order is instruction order number.
1. `Stack` ordinary stack, which inherits from `list`.

## [InstructionsCollection](IPPInter/InstructionsCollection.py)

Custom iterable class that takes list of `BaseInstruction` classes as parameter in constructor. This class has ability to jump back to instruction with appropriate order number. See `jump_to_inst` method in [InstructionsCollection](IPPInter/InstructionsCollection.py). 

## [InterpretCustomExceptions.py](IPPInter/InterpretCustomExceptions.py)

In this file are custom exceptions. One `IPPBaseException` which inherits `Exception` and has `ExitCode` field. Other, more specific, exceptions inherits from this base class and override the `ExitCode` field. 

## [Instruction](IPPInter/Instructions/Instruction.py)

Abstract base instruction class `BaseInstruction` is the base for each instruction. All the instructions inherits from this class (either directly or indirectly). It has `opCode` field, `arg1`, `arg2`, `arg3` fields, which `Argument` instances and are set to `Non` at the beginning, `argc` method that returns number of arguments it has.
2 private methods `__check_sort_set_arg__`, which inits the `arg1`, `arg2`, `arg3` fields according to `count` parameter at the end calls the abstract method `__set_arg__` and `__check_operand_types__`, which checks operand types. 2 abstract methods `__set_arg__` and `do`. All classes that inherit this class should handle setting their arguments to appropriate non terminal symbol in `__set_arg__`.
`do` abstract method take one parameter `stacks`, so the instructions can operate with them and returns `tuple, order` where the tuple is `(jump_flag, return_jump_flag)` and `order` is order of instruction to jump to (if `jump` flag is not set this number is irrelevant).
For more info see [BaseInstruction](IPPInter/Instructions/Instruction.py)

`TSymSymBase` is abstract base class that inherits from `BaseInstruction`. It represents most used instructions where the the first non term symbol is instruction specific (default is variable) and the other too are symbols. Number of arguments is by default set to 3 but some instructions like _NOT_ have only 2 arguments, so this can be overridden.

## [InstructionFactory](IPPInter/Instructions/InstructionFactory.py)

Factory pattern. `instruction_factory` method, that returns instance of a class that inherits from `BaseInstruction` if instruction `op_Code` equals supplied op_code.

## Individual instructions

Individual instructions inherit from `BaseInstruction` either directly and indirectly. They execute operations according to requirements. Their implementation is straightforward and they can be found in _IPPInter/Instructions_ folder:
* [Arithmetic](IPPInter/Instructions/Arithmetic.py)
* [DataStack](IPPInter/Instructions/DataStack.py)
* [Debug](IPPInter/Instructions/Debug.py)
* [FrameFunc](IPPInter/Instructions/FrameFunc.py)
* [IO](IPPInter/Instructions/IO.py)
* [ProgramFlow](IPPInter/Instructions/ProgramFlow.py)
* [String](IPPInter/Instructions/String.py)
* [Type](IPPInter/Instructions/Type.py)

# Test framework

## How to run

`php test.php [--help|-h] [--directory=path|-d=path] [--recursive|-r] [--parse-script] [--int-script] [--parse-only] [--int-only] [--jexamxml=file]`
* `--help|-h`                   prints help to standard output.
* `--directory=path|-d=path`    directory containing tests. If it is not supplied the path is set to './'.
* `--recursive|-r`              recursive search for tests.
* `--parse-script`              parse script file for analysis of IPPcode20 source code. If it is not supplied the default file is './parse.php'.
* `--int-script`                interpret script file for interpreting of XML representation of IPPcode20 source code. If it is not supplied the default file is './interpret.py'.
* `--parse-only`                test only parse.php. Cannot be combined with --int-only.
* `--int-only`                  test only interpret.py. Cannot be combined with --parse-only.
* `--jexamxml=file`             file with JAR file with A7Soft JExamlXML tool. If not supplied the location is '/pub/courses/ipp/jexamxml/jexamxml.jar'"

## [test.php](test.php)

Main script script for test framework, which checks the validity of parameters and their variance validity. It creates `IPPTester` instance and calls its `Test` method and also creates `htmlGenerator` instance and passes output from `IPPTester` `Test` method to `htmlGenerator` instance `Generate` method.

## [IPPTester](IPPTester.php)

`IPPTester` class executes the tests. At first it sets the flags and fields from arguments. Creates directory iterator and runs test for each _.src_ file in supplied directory recursively or non-recursively (depends on the `--recursive` option). For the files that does not exits, creates them and
puts a default value in. After that it which option of test to use (both, parser only or interpret only), creates cmd for the script to test and executes it. Afterwards the result is put into .rc file. If the result is non zero value only .rc files are compared by `diff` tool (with `-Z --strip-trailing-cr` to ignore windows CR and ignore trailing whitespace).
If the result is 0 the output from the script is redirected into temporary _.out_tmp_ file and compared with expected output in _.out_ file. Afterwards the temporary file is deleted. The `--parse-only` options use jexamxml tool to compare output XML files. Option `--int-only` tests possible redirection of input and source option (results from one test is gather, so there are no duplicates).
Option `both` creates more temporary files as the output XML from parser need to be redirected to interpret. Test results are than gather into dictionary, which looks like {"path/to/test/file.src" => bool}

## [htmlGenerator](htmlGenerator.php)

Generates html report from supplied test dictionary. It groups test into so called _test suites_ test suit is considered a folder, where the test file is located. Created html has a header with a style and body, where is:
1. Summary percentage of passed tests and summary table.
1. Table of contents of test suites and indication if all the tests has passed.
1. Individual test suites with percentage of passed tests, its summary table and hyper-links to test files.