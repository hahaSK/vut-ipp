<?php

class TestMessages
{
    public static string $HelpMessage = "Script test.php does automatic tests of parse.php and interpret.py.
		It checks their return codes and generated outputs with references.
		This test script works with 4 files. *.src *.in *.out *.rc.
		usage: php test.php [--help|-h] [--directory=path|-d=path] [--recursive|-r] [--parse-script] [--int-script] [--parse-only] [--int-only] [--jexamxml=file]
		  `--help|-h` prints help to standard output.
		  `--directory=path|-d=path` directory containing tests. If it is not supplied the path is set to './'.
		  `--recursive|-r` recursive search for tests.
		  `--parse-script` parse script file for analysis of IPPcode20 source code. If it is not supplied the default file is './parse.php'.
		  `--int-script` interpret script file for interpreting of XML representation of IPPcode20 source code. If it is not supplied the default file is './interpret.py'.
		  `--parse-only` test only parse.php. Cannot be combined with --int-only.
          `--int-only` test only interpret.py. Cannot be combined with --parse-only.
          `--jexamxml=file` file with JAR file with A7Soft JExamlXML tool. If not supplied the location is '/pub/courses/ipp/jexamxml/jexamxml.jar'",
        $DirectoryNotFound = "Specified directory does not exists or is invalid.";
}