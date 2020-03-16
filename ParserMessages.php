<?php

/**
 * VUT FIT IPP 2019/2020 project.
 *
 * ParserMessages class.
 *
 * @author Ing. Juraj lahvička, xlahvi00 <xlahvi00@vutbr.cz>
 */

declare(strict_types=1);

/**
 * Class ParserMessages contains General messages
 */
class ParserMessages
{
    public static string $HeaderFileErrMessage = "Wrong or missing header .IPPcode20",
        $ParserHelpMessage = "Script parse.php loads IPPcode20 source code from standard input,
		checks lexical and syntactic rules and prints XML representation
		of program to standard output.
		usage: php parse.php [--help|-h] [--stats=file] [--loc] [--comments] [--labels] [--jumps]
		  `--help|-h` prints help to standard output.
		  `--stats=file` prints statistics to the file.
		  `--loc` prints number of lines with instructions to statistics. --stats must be set.
		  `--comments` prints number of lines with comments to statistics. --stats must be set.
		  `--labels` prints number of labels in code to statistics. --stats must be set.
		  `--jumps` prints number of jumps in code to statistics. --stats must be set.",
        $OutputFileErrMessage = "Couldn't open/create/write to/close output file: ";
}