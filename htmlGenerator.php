<?php

/**
 * VUT FIT IPP 2019/2020 project.
 *
 * HTMLGenerator class.
 *
 * @author Ing. Juraj lahvička, xlahvi00 <xlahvi00@vutbr.cz>
 */

declare(strict_types=1);

/**
 * Class htmlGenerator Generates html report.
 */
class htmlGenerator
{
    private string $_header = '<!DOCTYPE html> 
                                <html lang="en">
                                <head>
                                <title>IPP20 test results</title>
                                <style>
                                body, html {height: 100%; margin-top: 0;}
                                .TestSuiteBody {padding-left: 40px;}
                                .OK {color: green;}
                                .FAILED {color: red;}
                                th {border: black dotted thin;}
                                tr {border: black solid thin;}
                                #Summary {background: lightgray; text-align: center;}
                                #Summary table {margin: auto;}
                                #TableOfContent {text-align: center;}
                                #TableOfContent table {margin: auto; border: black dotted thin;}
                                #TableOfContent table th, #TableOfContent table tr {border: 0; border-bottom: black dotted thin;}
                                #TableOfContent p {margin: 2px auto; }
                                a {text-decoration: none;}
                                </style>
                                </head>';

    private string $_testSuits = '<div id="suites">';

    /**
     * @brief Generates the html from test dictionary. The last folder is considered as test suit name.
     *
     * @param array $tests dictionary pf tests where key is the path to the test and value is result.
     * @return string generated html
     */
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
            //Divide the test path into folders and file name
            $exploded = array_map('strrev', explode('/', strrev($test)));
            $file = $exploded[0];
            if (sizeof($exploded) <= 1)
                $testSuite = './';
            else
                $testSuite = $exploded[1];

            //Check if the test is in different test suite => different folder.
            if ($testSuite != $lastTestSuite) {
                if (!$firstTest) {
                    //Complete the suite html
                    $this->completeSuite($suites, $suiteBody, array("passed" => $testSuitePassedCount, "failed" => $testSuiteNotPassedCount, "total" => $testSuiteTestCount));
                    //Add the suite to table of content array
                    $tableOfContentArr[$lastTestSuite] = ($testSuiteTestCount == $testSuitePassedCount);

                    //Reset the suite body
                    $suiteBody = '';
                    //And the counters
                    $testSuitePassedCount = $testSuiteNotPassedCount = $testSuiteTestCount = 0;
                }

                //Create new suite header
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

        //Need to close the last test suite
        $this->completeSuite($suites, $suiteBody, array("passed" => $testSuitePassedCount, "failed" => $testSuiteNotPassedCount, "total" => $testSuiteTestCount));
        $this->_testSuits .= '</div>';

        $tableOfContentArr[$lastTestSuite] = ($testSuiteTestCount == $testSuitePassedCount);

        return $this->_header . '<body>' . $this->summaryTable($passedCount, $notPassedCount, count($tests)) . $this->tableOfContent($tableOfContentArr) . $suites . '</body>';
    }

    /**
     * @brief Method that adds the test into appropriate div.
     *
     * @param string $test test name
     * @param bool $passed
     * @param string $suiteDiv suite block to add into
     */
    private function addToTestSuite(string $test, bool $passed, string &$suiteDiv)
    {
        $status = $passed ? 'OK' : 'FAILED';
        $suiteDiv .= "<p class='$status TestSuiteBody'><a href=\"$test\"'>$test</a>..............$status</p>" . PHP_EOL;
    }

    /**
     * @param int $count
     * @param int $total
     * @return false|float
     */
    private function calcPercentage(int $count, int $total)
    {
        $passedPercentage = ($count / $total) * 100;

        if (is_nan($passedPercentage))
            $passedPercentage = 100;

        return round($passedPercentage, 2);
    }

    /**
     * @brief method that generates suite summary table.
     *
     * @param int $passedCount number of passed tests in the suite
     * @param int $notPassedCount number of failed tests in the suite
     * @param int $total number of tests in the suite
     * @return string html string of suite summary table
     */
    private function suiteSummaryTable(int $passedCount, int $notPassedCount, int $total)
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

    /**
     * @brief method that generates summary table for all the test suites.
     *
     * @param int $passedCount total number of passed tests in all suites
     * @param int $notPassedCount total number of failed tests in all suites
     * @param int $total total number of tests in all suites
     * @return string html string of summary table for all suites
     */
    private function summaryTable(int $passedCount, int $notPassedCount, int $total)
    {
        $passedPercentage = $this->calcPercentage($passedCount, $total);
        return "<div id='Summary'>
                    <h1 style='margin-top: 0;'>$passedPercentage% Passed</h1>
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

    /**
     * @brief method completes the suite div.
     *
     * @param string $suites suites html div
     * @param string $suiteBody current suite body
     * @param array $counts array of all the counts for the suite.
     */
    private function completeSuite(string &$suites, string $suiteBody, array $counts)
    {
        $suites .= $this->suiteSummaryTable($counts["passed"], $counts["failed"], $counts["total"]);
        $suites .= $suiteBody;
        $suites .= '</div>';
    }

    /**
     * @brief Method creates table of content from all the suites and hyper-links to them.
     *
     * @param array $arrayOfContent array of all the suites
     * @return string table of content in html
     */
    private function tableOfContent(array &$arrayOfContent)
    {
        $tableOfContent = '<div id="TableOfContent">
                                <h2>Table of Content</h2>
                                <table>';
        foreach ($arrayOfContent as $suite => $status) {
            $suiteStatus = ($status) ? 'OK' : 'FAILED';
            $tableOfContent .= "<tr>
                                    <th><a href='#$suite'>$suite</a></th>
                                    <th><p class='$suiteStatus'>$suiteStatus</p></th>
                                </tr>";
        }
        return $tableOfContent . '</table></div>';
    }
}