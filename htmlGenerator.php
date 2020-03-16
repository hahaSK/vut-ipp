<?php

declare(strict_types=1);

class htmlGenerator
{
    private string $_header = '<!DOCTYPE html> 
                                <html lang="en">
                                <head><title>IPP20 test results</title></head>';

    private string $_passed = '<h2>Passed</h2>
                                <div class="passed>';
    private string $_notPassed = '<h2>Not Passed</h2>
                                  <div class="notPassed>';

    public function Generate($tests)
    {
        var_dump($tests);
        $passedCount = $notPassedCount = 0;
        foreach ($tests as $test => $value) {
            if ($value) {
                ++$passedCount;
                $this->appendToDiv($test, $this->_passed);
            } else {
                ++$notPassedCount;
                $this->appendToDiv($test, $this->_notPassed);
            }
        }
        $this->_passed .= '</div>';
        $this->_notPassed .= '</div>';

        return $this->_header . $this->summaryTable($passedCount, $notPassedCount, count($tests)) . $this->_passed . $this->_notPassed;
    }

    private function appendToDiv(string $test, string &$testDiv)
    {
        $testDiv .= "<a href=\"$test\">$test</a><br>" . PHP_EOL;
    }

    private function table(int $passedCount, int $notPassedCount, int $count)
    {
        $passedPercentage = $passedCount / $count;

        return "<h1>$passedPercentage% Passed</h1>
                <table>
                    <tr>
                        <th>Passed</th>
                        <th>Not passed</th>
                        <th>Tests total</th>
                    </tr>
                    <tr>
                        <th>$passedCount</th>
                        <th>$notPassedCount</th>
                        <th>$count</th>
                    </tr>
                </table>";
    }
}