<?php

declare(strict_types=1);

class htmlGenerator
{
    private string $_header = '<!DOCTYPE html> 
                                <html lang="en">
                                <head>
                                <title>IPP20 test results</title>
                                <style>
                                .TestSuiteBody {padding-left: 40px;}
                                .OK {color: green;}
                                .FAILED {color: red;}
                                th {border: black dotted thin;}
                                tr {border: black solid thin;}
                                #Summary {background: lightgray; text-align: center;}
                                #Summary table {margin: auto;}
                                #TableOfContent {text-align: center;}
                                </style>
                                </head>';

    private string $_testSuits = '<div id="suites">';

    public function Generate($tests)
    {
        $passedCount = $notPassedCount = 0;
        $testSuitePassedCount = $testSuiteNotPassedCount = $testSuiteTestCount = 0;
        $lastTestSuite = './';
        $suites = '';
        $suiteBody = '';
        $firstTest = true;

        $tableOfContentArr = array();
        foreach ($tests as $test => $value) {
            $exploded = array_map('strrev', explode('/', strrev($test)));
            $file = $exploded[0];
            if (sizeof($exploded) <= 1)
                $testSuite = './';
            else
                $testSuite = $exploded[1];

            if ($testSuite != $lastTestSuite) {
                if (!$firstTest) {
                    $this->completeSuite($suites, $suiteBody, array("passed" => $testSuitePassedCount, "failed" => $testSuiteNotPassedCount, "total" => $testSuiteTestCount));

                    $tableOfContentArr[$lastTestSuite] = ($testSuiteTestCount == $testSuitePassedCount);

                    $suiteBody = '';
                    $testSuitePassedCount = $testSuiteNotPassedCount = $testSuiteTestCount = 0;
                }

                $suites .= "<div class=\"TestSuite\">
                                <h2 id='$testSuite'>test suite: $testSuite</h2>";
                $firstTest = false;
                $lastTestSuite = $testSuite;

                $tableOfContentArr[$testSuite] = false;
            }

            if ($value) {
                ++$passedCount;
                ++$testSuitePassedCount;
                $this->addToTestSuite($test, true, $suiteBody);
            } else {
                ++$notPassedCount;
                ++$testSuiteNotPassedCount;
                $this->addToTestSuite($test, false, $suiteBody);
            }
            ++$testSuiteTestCount;
        }

        $this->completeSuite($suites, $suiteBody, array("passed" => $testSuitePassedCount, "failed" => $testSuiteNotPassedCount, "total" => $testSuiteTestCount));
        $this->_testSuits .= '</div>';

        $tableOfContentArr[$lastTestSuite] = ($testSuiteTestCount == $testSuitePassedCount);

        return $this->_header . $this->summaryTable($passedCount, $notPassedCount, count($tests)) . $this->tableOfContent($tableOfContentArr) . $suites;
    }

    private function addToTestSuite(string $test, bool $passed, string &$suiteDiv)
    {
        $status = $passed ? 'OK' : 'FAILED';
        $suiteDiv .= "<p class='$status TestSuiteBody'><a href=\"$test\"'>$test</a>..............$status</p>" . PHP_EOL;
    }

    private function calcPercentage(int $count, int $total)
    {
        $passedPercentage = ($count / $total) * 100;

        if (is_nan($passedPercentage))
            $passedPercentage = 100;

        return round($passedPercentage, 2);
    }

    private function suitSummaryTable(int $passedCount, int $notPassedCount, int $total)
    {
        $passedPercentage = $this->calcPercentage($passedCount, $total);
        return "<h4 class='TestSuiteBody'>$passedPercentage% Passed</h4>
                <table class='TestSuiteBody'>
                    <tr>
                        <th style='color: green'>Passed</th>
                        <th style='color: red'>Not passed</th>
                        <th>Tests total</th>
                    </tr>
                    <tr>
                        <th style='color: green'>$passedCount</th>
                        <th style='color: red'>$notPassedCount</th>
                        <th>$total</th>
                    </tr>
                </table>";
    }

    private function summaryTable(int $passedCount, int $notPassedCount, int $total)
    {
        $passedPercentage = $this->calcPercentage($passedCount, $total);
        return "<div id='Summary'>
                    <h1>$passedPercentage% Passed</h1>
                    <table>
                        <tr>
                            <th style='color: green'>Passed</th>
                            <th style='color: red'>Not passed</th>
                            <th>Tests total</th>
                        </tr>
                        <tr>
                            <th style='color: green'>$passedCount</th>
                            <th style='color: red'>$notPassedCount</th>
                            <th>$total</th>
                        </tr>
                    </table>
                </div>";
    }

    private function completeSuite(string &$suites, string $suiteBody, array $counts)
    {
        $suites .= $this->suitSummaryTable($counts["passed"], $counts["failed"], $counts["total"]);
        $suites .= $suiteBody;
        $suites .= '</div>';
    }

    private function tableOfContent(array &$arrayOfContent)
    {
        $tableOfContent = '<div id="TableOfContent">
                                <h2>Table of Content</h2>';
        foreach ($arrayOfContent as $suite => $status)
        {
            $suiteStatus = ($status) ? 'OK' : 'FAILED';
            $tableOfContent .= "<p class='$suiteStatus'><a href='#$suite'>$suite</a>....$suiteStatus</p>";
        }
        return $tableOfContent . '</div>';
    }
}