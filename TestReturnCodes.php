<?php

/**
 * VUT FIT IPP 2019/2020 project.
 *
 * ReturnCode class.
 *
 * @author Ing. Juraj lahvička, xlahvi00 <xlahvi00@vutbr.cz>
 */

declare(strict_types=1);

/**
 * Class TestReturnCodes for handling exiting and message printing.
 */
class TestReturnCodes
{
    public static function ParameterError()
    {
        self::printMessage(TestMessages::$HelpMessage);
        exit(10);
    }

    public static function InputFileError(string $directory, string $message)
    {
        self::printMessage($message . " '" . $directory . "'");
        exit(11);
    }

    /**
     * @param string $filePath file path of the output file.
     */
    public static function OutputFileError(string $filePath)
    {
        self::printMessage(TestMessages::$OutputFileErrMessage . $filePath . ".");
        exit(12);
    }

    /**
     * @param string $message message for internal error.
     */
    public static function InternalError(string $message)
    {
        self::printMessage($message);
        exit(99);
    }

    public static function HeaderFileError()
    {
        self::printMessage(TestMessages::$HeaderFileErrMessage);
        exit(21);
    }

    /**
     * @param int $lineNumber line number at which the error occurred.
     * @param string $instruction instruction/line at which the error occurred.
     */
    public static function OperationCodeError(int $lineNumber, string $instruction)
    {
        self::printMessage("Wrong Operation code at line " . $lineNumber . ". Instruction: " . $instruction);
        exit(22);
    }

    /**
     * @param int $lineNumber line number at which the error occurred.
     * @param string $opCode specific operation code at the which the error occurred.
     * @param array $operands operands for the specific operation code.
     */
    public static function LexicalSyntacticalError(int $lineNumber, string $opCode, array $operands)
    {
        $instOperands = "";
        foreach ($operands as $operand)
            $instOperands .= '<' . $operand . '> ';

        self::printMessage("Lexical or syntactical error at line: " . $lineNumber . ". Instruction for the operation code is: " . $opCode . " " . $instOperands);
        exit(23);
    }

    public static function Success()
    {
        exit(0);
    }

    /**
     * Print helper method.
     *
     * @param string $message message to print.
     */
    private static function printMessage(string $message)
    {
        fwrite(STDERR, strpos($message, PHP_EOL) ? $message : $message . PHP_EOL);
    }
}