<?php

/**
 * VUT FIT IPP 2019/2020 project.
 *
 * Parsing starter code.
 *
 * @author Ing. Juraj lahvička, xlahvi00 <xlahvi00@vutbr.cz>
 */

declare(strict_types=1);
include("Options.php");
include("IPPCodeParser.php");

$options = getopt($shortOpts, $longOpts);

if (isset($options["help"]) or isset($options["h"])) {
    fwrite(STDOUT, ParserMessages::$ParserHelpMessage . PHP_EOL);
    ParserReturnCodes::Success();
}

if (!isset($options["stats"]) && (isset($options["loc"]) || isset($options["comments"]) || isset($options["labels"]) || isset($options["jumps"])))
    ParserReturnCodes::ParameterError();


fwrite(STDOUT, IPPCodeParser::Parse($options)->saveXML());

ParserReturnCodes::Success();
