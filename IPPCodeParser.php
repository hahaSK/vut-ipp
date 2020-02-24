<?php

/**
 * VUT FIT IPP 2019/2020 project.
 *
 * IPPCodeParser class.
 *
 * @author Ing. Juraj lahvička, xlahvi00 <xlahvi00@vutbr.cz>
 */

declare(strict_types=1);
include("ReturnCodes.php");
include("XMLGenerator.php");


/**
 * Class IPPCodeParser for parsing IPPcode20 instruction source code.
 */
final class IPPCodeParser
{
    //Non terminal names
    private const varNonTerm = 'var',
        symbNonTerm = 'symb',
        labelNonTerm = 'label',
        typeNonTerm = 'type';

    //Patterns
    private const HEADER = '%^\s*(?i).IPPcode20' . self::COMMENT . '%',
        COMMENT = '\s*(#.*)?$',
        EMPTY_LINE = '%^\s*$%',

        //Data types
        TYPE_NIL = '(?:nil@nil)',
        TYPE_BOOL = '(?:bool@(?:true|false))',
        TYPE_INT = '(?:int@(?:-?|\+?)\d+)',
        TYPE_STRING = '(?:string@(?:[^\s#\\\\]|(?:\\\\\d{3}))*)', #for some reason the backslashes needs to be doubled

        CONST = '(?:' . self::TYPE_NIL . '|' . self::TYPE_BOOL . '|' . self::TYPE_INT . '|' . self::TYPE_STRING . ')',

        IDENTIFIER_SPECIAL_CHARS = '_\-\$\&\%\*\!\?',
        IDENTIFIER = '(?:[[:alpha:]' . self::IDENTIFIER_SPECIAL_CHARS . '][[:alnum:]' . self::IDENTIFIER_SPECIAL_CHARS . ']*)',

        LABEL = '(' . self::IDENTIFIER . ')',
        TYPE = '(int|bool|string)',
        VAR = '((?:GF|LF|TF)@' . self::IDENTIFIER . ')',
        SYMBOL = '(?:' . self::VAR . '|(' . self::CONST . '))';

    //Instructions syntax
    private const instructions = [
        //Frame
        "MOVE" => [self::varNonTerm, self::symbNonTerm],
        "CREATEFRAME" => [],
        "PUSHFRAME" => [],
        "POPFRAME" => [],
        "DEFVAR" => [self::varNonTerm],
        "CALL" => [self::labelNonTerm],
        "RETURN" => [],

        //Data stack
        "PUSHS" => [self::symbNonTerm],
        "POPS" => [self::varNonTerm],

        //Arithmetic
        "ADD" => [self::varNonTerm, self::symbNonTerm, self::symbNonTerm],
        "SUB" => [self::varNonTerm, self::symbNonTerm, self::symbNonTerm],
        "MUL" => [self::varNonTerm, self::symbNonTerm, self::symbNonTerm],
        "IDIV" => [self::varNonTerm, self::symbNonTerm, self::symbNonTerm],
        "LT" => [self::varNonTerm, self::symbNonTerm, self::symbNonTerm],
        "GT" => [self::varNonTerm, self::symbNonTerm, self::symbNonTerm],
        "EQ" => [self::varNonTerm, self::symbNonTerm, self::symbNonTerm],
        "AND" => [self::varNonTerm, self::symbNonTerm, self::symbNonTerm],
        "OR" => [self::varNonTerm, self::symbNonTerm, self::symbNonTerm],
        "NOT" => [self::varNonTerm, self::symbNonTerm],
        "INT2CHAR" => [self::varNonTerm, self::symbNonTerm],
        "STRI2INT" => [self::varNonTerm, self::symbNonTerm, self::symbNonTerm],

        //IO
        "READ" => [self::varNonTerm, self::typeNonTerm],
        "WRITE" => [self::symbNonTerm],

        //String operations
        "CONCAT" => [self::varNonTerm, self::symbNonTerm, self::symbNonTerm],
        "STRLEN" => [self::varNonTerm, self::symbNonTerm],
        "GETCHAR" => [self::varNonTerm, self::symbNonTerm, self::symbNonTerm],
        "SETCHAR" => [self::varNonTerm, self::symbNonTerm, self::symbNonTerm],

        //Type
        "TYPE" => [self::varNonTerm, self::symbNonTerm],

        //Program flow
        "LABEL" => [self::labelNonTerm],
        "JUMPIFEQ" => [self::labelNonTerm, self::symbNonTerm, self::symbNonTerm],
        "JUMPIFNEQ" => [self::labelNonTerm, self::symbNonTerm, self::symbNonTerm],
        "JUMP" => [self::labelNonTerm],
        "EXIT" => [self::symbNonTerm],

        //Debugging
        "DPRINT" => [self::symbNonTerm],
        "BREAK" => []
    ];


    /**
     * Parses the input and returns created DOM document.
     *
     * @param array $arguments input arguments.
     * @return DOMDocument generated DOM document.
     */
    public static function Parse(array $arguments): DOMDocument
    {
        $xmlGen = new XMLGenerator();
        $header = false;
        $stats = isset($arguments['stats']);
        $labels = array();
        $lineNumber = $instructionCount = $commentsCount = $jumpsCount = 0;
        while (($line = fgets(STDIN)) != false) {
            ++$lineNumber;
            //region Header
            if (self::isEmptyLine($line)) {
                continue;
            }
            if (self::isComment($line)) {
                ++$commentsCount;
                continue;
            }
            if (!$header) {
                if (self::isHeader($line, $commentsCount)) {
                    $header = true;
                    continue;
                } else
                    ReturnCodes::HeaderFileError();
            }
            //endregion

            $invalidInstruction = true;
            foreach (self::instructions as $opCode => $operands) {
                if (self::isValidOpCode($line, $opCode, $matches)) {
                    $invalidInstruction = false;
                    ++$instructionCount;
                    if (isset($matches[2]))
                        ++$commentsCount;
                    if (!self::parsOperands($operands, $matches[1], $parsedOperands))
                        ReturnCodes::LexicalSyntacticalError($lineNumber, $opCode, $operands);

                    array_shift($parsedOperands); //remove 0th element
                    $xmlGen->AddInstruction($opCode, $parsedOperands);

                    if ($stats)
                        self::labelStatistics($opCode, $parsedOperands, $labels);

                    if (in_array($opCode, ['CALL', 'RETURN', 'JUMP', 'JUMPIFEQ', 'JUMPIFNEQ']))
                        ++$jumpsCount;

                    break;
                }
            }
            if ($invalidInstruction)
                ReturnCodes::OperationCodeError($lineNumber, $line);
        }

        if (!$header)
            ReturnCodes::HeaderFileError();

        if ($stats)
            self::writeStats($arguments["stats"], $arguments, $instructionCount, $commentsCount, count($labels), $jumpsCount);

        return $xmlGen->GetDocument();
    }

    /**
     * Checks if line is empty.
     *
     * @param string $line instruction/line to check.
     * @return bool return true if pattern matches empty line otherwise false.
     */
    private static function isEmptyLine(string $line): bool
    {
        return (bool)preg_match(self::EMPTY_LINE, $line);
    }

    /**
     * Checks if line is comment.
     *
     * @param string $line instruction/line to check.
     * @return bool return true if pattern matches comment otherwise false.
     */
    private static function isComment(string $line): bool
    {
        return (bool)preg_match('%^' . self::COMMENT . '%', $line);
    }

    /**
     * Checks header validity.
     *
     * @param string $line instruction/line to check.
     * @param int $commentsCount if header contains comment increments comments count.
     * @return bool return true if pattern matches header otherwise false.
     */
    private static function isHeader(string $line, int &$commentsCount): bool
    {
        $isHeader = (bool)preg_match(self::HEADER, $line, $matches);
        if (isset($matches) && isset($matches[1]))
            ++$commentsCount;
        return $isHeader;
    }

    /**
     * Checks operation code validity.
     *
     * @param string $line instruction/line to check.
     * @param string $opCode operation code to match.
     * @param string[] $matches results of the search.
     * @return bool return true if pattern matches operation code otherwise false.
     */
    private static function isValidOpCode(string $line, string $opCode, &$matches): bool
    {
        return (bool)preg_match('%^(?i)\s*' . $opCode . '([^#]*)' . self::COMMENT . '%', $line, $matches);
    }

    /**
     * Parses the operands from the operands string (input instruction).
     *
     * @param string[] $operands operands to match.
     * @param string $opString instruction string without operation code. In other words operands string.
     * @param string[] $parsedOperands parsed operands.
     * @return bool return true if pattern matches operation code's syntax and parsing was successful otherwise false.
     */
    private static function parsOperands($operands, $opString, &$parsedOperands): bool
    {
        $operandsPattern = '%^';
        foreach ($operands as $operand) {
            switch ($operand) {
                case self::varNonTerm:
                    $operandsPattern .= '\s+' . self::VAR;
                    break;
                case self::typeNonTerm:
                    $operandsPattern .= '\s+' . self::TYPE;
                    break;
                case self::labelNonTerm:
                    $operandsPattern .= '\s+' . self::LABEL;
                    break;
                case self::symbNonTerm:
                    $operandsPattern .= '\s+' . self::SYMBOL;
                    break;

                default:
                    break;
            }
        }
        $operandsPattern .= '\s*$%';

        if (preg_match($operandsPattern, $opString, $parsedOperands)) {
            //Need to remove empty strings from the not found matches
            self::removeEmptyStrings($parsedOperands);
            return true;
        }
        return false;
    }

    /**
     * Removes empty strings from array.
     *
     * @param array $array array to remove empty strings from.
     */
    private static function removeEmptyStrings(array &$array): void
    {
        $array = array_values(array_filter($array, function (string $value, int $key) use ($array): bool {
            return $value !== '' || (isset($array[$key - 1]) && $array[$key - 1] === 'string');
        }, ARRAY_FILTER_USE_BOTH));
    }

    /**
     * Appends/adds unique labels to labels array parameter for statistic purposes.
     *
     * @param string $opCode operation code to check.
     * @param array $operands array of operands.
     * @param array $labels unique labels array.
     */
    private static function labelStatistics(string $opCode, array $operands, array &$labels)
    {
        if (!in_array(self::labelNonTerm, self::instructions[$opCode]) or !isset($operands))
            return;

        if (!in_array($operands[0], $labels))
            $labels[] = $operands[0];
    }

    /**
     * Writes specified statistics into file.
     *
     * @param string $filePath path to file to write the statistics into.
     * @param array $arguments input arguments.
     * @param int $instructionCount instruction counts.
     * @param int $commentsCount comments count.
     * @param int $labelCount labels count.
     * @param int $jumpsCount jumps count.
     */
    private static function writeStats(string $filePath, array $arguments, int $instructionCount, int $commentsCount, int $labelCount, int $jumpsCount)
    {
        if (!$filePath)
            return;

        if (!($fileHandle = fopen($filePath, 'w')))
            ReturnCodes::OutputFileError($filePath);

        foreach ($arguments as $key => $value) {
            $data = 0;
            switch ($key) {
                case 'loc':
                    $data = $instructionCount;
                    break;
                case 'comments':
                    $data = $commentsCount;
                    break;
                case 'labels':
                    $data = $labelCount;
                    break;
                case 'jumps':
                    $data = $jumpsCount;
                    break;

                default:
                    continue 2;
            }

            if (is_array($value)) {
                foreach ($value as $innerVal) {
                    if (fwrite($fileHandle, "$data\n") === false)
                        ReturnCodes::OutputFileError($filePath);
                }
            } else
                if (fwrite($fileHandle, "$data\n") === false)
                    ReturnCodes::OutputFileError($filePath);
        }

        if (!fclose($fileHandle))
            ReturnCodes::OutputFileError($filePath);
    }
}
