<?php

/**
 * VUT FIT IPP 2019/2020 project.
 *
 * IPPTester class.
 *
 * @author Ing. Juraj lahvička, xlahvi00 <xlahvi00@vutbr.cz>
 */

declare(strict_types=1);
include("TestMessages.php");
include("htmlGenerator.php");

/**
 * Class IPPTester for running selected tests and comparing results.
 */
final class IPPTester
{
    private const srcExt = 'src';

    private string $directory = '.';
    private bool $recursive = false, $parseOnly = false, $intOnly = false;
    private string $parseScript = './parse.php';
    private string $interpretScript = './interpret.py', $jexamxmlPath = "/pub/courses/ipp/jexamxml/jexamxml.jar";

    private array $tests = array();

    /**
     * @param SplFileInfo $current current file to test
     */
    private function doTest(SplFileInfo $current)
    {
        $inFile = str_replace('.' . self::srcExt, ".in", $current->getPathname());
        $outFile = str_replace('.' . self::srcExt, ".out", $current->getPathname());
        $rcFile = str_replace('.' . self::srcExt, ".rc", $current->getPathname());
        $outFileTemp = $outFile . "_tmp";
        $outXMLFileTemp = $outFile . ".xml" . "_tmp";
        $rcFileTemp = $rcFile . "_tmp";
        $srcFile = $current->getPathname();

        $testFiles = [$srcFile => '',
            $inFile => '',
            $outFile => '',
            $rcFile => '0',
            $outFileTemp => '',
            $rcFileTemp => ''];

        $intFiles = [
            'src' => $srcFile,
            'in' => $inFile,
            'outTmp' => $outFileTemp,
            'rcTmp' => $rcFileTemp,
            'rc' => $rcFile,
            'out' => $outFile
        ];

        //If file doesn't exist create and put a default value.
        foreach ($testFiles as $testFile => $testFileDefVal) {
            if (!file_exists($testFile))
                file_put_contents($testFile, $testFileDefVal);
        }

        $result = 0;
        //Test parser
        if ($this->parseOnly) {
            $cmd = "\"php7.4\" \"$this->parseScript\" < \"$srcFile\" > \"$outFileTemp\"";
            exec($cmd, $output, $result);
            file_put_contents($rcFileTemp, $result);
            if ($result != 0)
                exec("diff -Z \"$rcFileTemp\" \"$rcFile\"", $output, $result);
            else {
                exec("diff -Z \"$rcFileTemp\" \"$rcFile\"", $output, $resultRC);
                exec("java -jar $this->jexamxmlPath $outFile $outFileTemp", $output, $resultOUT);
                $result = ($resultRC == 0 && $resultOUT == 0) ? 0 : 1;
            }
        } else if ($this->intOnly) {
            $result = $this->testInterpret($intFiles);
        } else {
            //Test parser
            $cmd = "\"php7.4\" \"$this->parseScript\" < \"$srcFile\" > \"$outXMLFileTemp\"";
            exec($cmd, $output, $result);
            if ($result != 0) {
                file_put_contents($rcFileTemp, $result);
                exec("diff -Z \"$rcFileTemp\" \"$rcFile\"", $output, $result);
            } else {
                $intFiles['src'] = $outXMLFileTemp;
                $result = $this->testInterpret($intFiles);
            }
            //Remove temporary XML file
            $this->removeTmpFile($outXMLFileTemp);
        }
        //Put the test path to test dictionary, where key is the path and the value is result
        $this->tests += [str_replace('\\', '/', $srcFile) => ($result == 0) ? true : false];
        $this->removeTmpFile($outFileTemp);
        $this->removeTmpFile($rcFileTemp);
    }

    /**
     * @brief method to start the tests.
     *
     * @param array $arguments
     * @return array dictionary of test results, where key is path to the test .src and value is result
     */
    public function Test(array $arguments): array
    {
        $this->GetArgs($arguments);

        $it = null;
        try {
            if ($this->recursive)
                $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($this->directory));
            else
                $it = new RecursiveDirectoryIterator($this->directory);
        } catch (UnexpectedValueException $exception) {
            TestReturnCodes::InputFileError($this->directory, TestMessages::$DirectoryNotFound);
        }

        if ($it == null)
            TestReturnCodes::InternalError("File Iterator is null!");

        $it->rewind();
        while ($it->Valid()) {
            if (!$it->isDot()) {
                //Non recursive is also taking directories => need to exclude them
                if (!$this->recursive and is_dir($it->getPathname())) {
                    $it->next();
                    continue;
                }

                if ($it->getExtension() === self::srcExt)
                    self::doTest($it->current());
            }
            $it->next();
        }
        return $this->tests;
    }

    /**
     * @brief parse arguments.
     *
     * @param array $arguments
     */
    private function GetArgs(array $arguments): void
    {
        if (isset($arguments["directory"]))
            $this->directory = $arguments["directory"];
        else if (isset($arguments["d"]))
            $this->directory = $arguments["d"];

        if (!is_dir($this->directory))
            TestReturnCodes::InputFileError($this->directory, TestMessages::$DirectoryNotFound);

        $this->recursive = (isset($arguments["recursive"]) or isset($arguments["r"]));
        if (isset($arguments['parse-script']))
            $this->parseScript = $arguments["parse-script"];

        if (isset($arguments["int-script"]))
            $this->interpretScript = $arguments["int-script"];

        $this->parseOnly = isset($arguments["parse-only"]);
        $this->intOnly = isset($arguments["int-only"]);

        if (isset($arguments["jexamxml"]))
            $this->jexamxmlPath = $arguments["jexamxml"];
    }

    /**
     * @param string $tmpFile
     */
    private function removeTmpFile(string $tmpFile): void
    {
        if (!unlink($tmpFile))
            TestReturnCodes::InternalError("Cannot delete temporary file $tmpFile");
    }

    /**
     * @brief tests the interpret with all 3 parameter variations
     *
     * @param array $files for interpret test
     * @return int result of the test
     */
    private function testInterpret(array $files): int
    {
        $srcFile = $files['src'];
        $inFile = $files['in'];
        $outFileTemp = $files['outTmp'];
        $rcFileTemp = $files['rcTmp'];
        $rcFile = $files['rc'];
        $outFile = $files['out'];

        $cmd = "\"python3.8\" \"$this->interpretScript\" \"--input=$inFile\" < \"$srcFile\"  > \"$outFileTemp\"";
        exec($cmd, $output, $resultInRed);

        $cmd = "\"python3.8\" \"$this->interpretScript\" \"--source=$srcFile\" < \"$inFile\" > \"$outFileTemp\"";
        exec($cmd, $output, $resultSourceRed);

        $cmd = "\"python3.8\" \"$this->interpretScript\" \"--source=$srcFile\" \"--input=$inFile\" > \"$outFileTemp\"";
        exec($cmd, $output, $result);

        if ($result != $resultSourceRed or $result != $resultInRed)
            return 1;

        file_put_contents($rcFileTemp, $result);
        if ($result != 0)
            exec("diff -Z --strip-trailing-cr \"$rcFileTemp\" \"$rcFile\"", $output, $result);
        else {
            exec("diff -Z --strip-trailing-cr \"$rcFileTemp\" \"$rcFile\"", $output, $resultRC);
            exec("diff -Z --strip-trailing-cr \"$outFileTemp\" \"$outFile\"", $output, $resultOUT);
            return ($resultRC == 0 && $resultOUT == 0) ? 0 : 1;
        }
        return $result;
    }

}