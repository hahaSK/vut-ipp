<?php

declare(strict_types=1);
include("TestOptions.php");
include("TestReturnCodes.php");
include("IPPTester.php");

$options = getopt($ShortOpt, $LongOpt);

if (isset($options["help"]) or isset($options["h"])){
    fwrite(STDOUT, TestMessages::$HelpMessage . PHP_EOL);
    TestReturnCodes::Success();
}

if (isset($options["parse-only"]) and (isset($options["int-only"]) or isset($options["int-script"])))
    TestReturnCodes::ParameterError();
if (isset($options["int-only"]) and (isset($options["parse-only"]) or isset($options["parse-script"])))
    TestReturnCodes::ParameterError();

$tester = new IPPTester();
$htmlGen = new htmlGenerator();
fwrite(STDOUT, $htmlGen->Generate($tester->Test($options)));

TestReturnCodes::Success();
