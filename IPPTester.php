<?php

declare(strict_types=1);
include("TestMessages.php");
include("htmlGenerator.php");

final class IPPTester
{
    private const srcExt = 'src';

    private string $directory = '.';
    private bool $recursive = false, $parseOnly = false, $intOnly = false;
    private string $parseScript = './parse.php';
    private string $interpretScript = './interpret.py', $jexamxmlPath = "/pub/courses/ipp/jexamxml/jexamxml.jar";

    private array $tests = array();

    private function doTest(SplFileInfo $current)
    {
        $inFile = str_replace('.' . self::srcExt, ".in", $current->getPathname());
        $outFile = str_replace('.' . self::srcExt, ".out", $current->getPathname());
        $rcFile = str_replace('.' . self::srcExt, ".rc", $current->getPathname());
        $outTemp = $outFile . "_tmp";
        $srcFile = $current->getPathname();

        $testFiles =  [$srcFile => '',
            $inFile  => '',
            $outFile => '',
            $rcFile => '0',
            $outTemp => ''];

        foreach ($testFiles as $testFile => $testFileDefVal)
        {
            if (!file_exists($testFile))
                file_put_contents($testFile, $testFileDefVal);
        }

        $result = 0;
        if ($this->parseOnly)
        {
            $cmd = "\"php\" \"$this->parseScript\" < \"$srcFile\" > \"$outTemp\"";
            exec($cmd, $output, $result);
            echo $rcFile;
            if ($result != 0)
                exec("diff $result \"$rcFile\"", $output, $result);
            else
                exec("$this->jexamxmlPath $outFile $outTemp", $output, $result);
        }
        else if ($this->intOnly)
        {
            throw new Exception("Not implemented");
//            $cmd = "\"php.exe\" \"$this->interpretScript\" < \"$srcFile\" > \"$outTemp\"";
//            exec($cmd, $output, $result);
//            if ($result != 0)
//                exec("diff $result \"$rcFile\"", $output, $result);
//            else
//                exec("diff $outFile $outTemp", $output, $result);
        }
        else
        {
            throw new Exception("Not implemented");
        }

        $this->tests += [str_replace('\\', '/', $srcFile) => ($result == 0) ? true : false];
        if (!unlink($outTemp))
            TestReturnCodes::InternalError("Cannot delete temporary file $outTemp");
    }

    public function Test(array $arguments) : array
    {
        $this->GetArgs($arguments);

        $it = null;
        try {
            if ($this->recursive)
                $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($this->directory));
            else
                $it = new RecursiveDirectoryIterator($this->directory);
        }
        catch (UnexpectedValueException $exception) {
            TestReturnCodes::InputFileError($this->directory, TestMessages::$DirectoryNotFound);
        }

        if ($it == null)
            TestReturnCodes::InternalError("File Iterator is null!");

        $it->rewind();
        while ($it->Valid())
        {
            if (!$it->isDot())
            {
                //Non recursive is also taking directories => need to exclude them
                if (!$this->recursive and is_dir($it->getPathname()))
                {
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

}