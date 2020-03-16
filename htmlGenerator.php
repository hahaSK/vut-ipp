<?php

declare(strict_types=1);

class htmlGenerator
{
    private string $_header = '<!DOCTYPE html> 
                                <html lang="en">
                                <head><title>IPP20 test results</title></head>';

    private string $_passed = '<div class="passed>';
    private string $_notPassed = '<div class="notPassed>';

    /**
     * htmlGenerator constructor.
     */
    public function __construct()
    {

    }

    public function Generate(array $tests)
    {
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
    }

    private function appendToDiv(string $test, string &$testDiv)
    {
        $testDiv .= "<a href=\"$test\">$test</a>";
    }
}