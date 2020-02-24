<?php

/**
 * VUT FIT IPP 2019/2020 project.
 *
 * XMLGenerator class class.
 *
 * @author Ing. Juraj lahvička, xlahvi00 <xlahvi00@vutbr.cz>
 */

declare(strict_types=1);

/**
 * Class XMLGenerator for generating XML document.
 */
class XMLGenerator
{
    private DOMElement $_root;
    private DOMDocument $_xml;
    private int $_instructionCount = 0;

    /**
     * XMLGenerator constructor.
     */
    public function __construct()
    {
        $this->_xml = new DOMDocument();

        $this->_xml->encoding = 'utf-8';
        $this->_xml->xmlVersion = '1.0';
        $this->_xml->formatOutput = true;

        $this->_root = $this->_xml->createElement('program');
        $this->_root->setAttributeNode(new DOMAttr("language", "IPPcode20"));
    }

    /**
     * Returns the generated document.
     *
     * @return DOMDocument created DOM document.
     */
    public function GetDocument(): DOMDocument
    {
        $this->_xml->appendChild($this->_root);
        return $this->_xml;
    }

    /**
     * Adds instruction into the XML file.
     *
     * @param string $instruction instruction to add.
     * @param array $operands operands of the instruction.
     */
    public function AddInstruction(string $instruction, array $operands): void
    {
        ++$this->_instructionCount;
        $insElem = $this->_xml->createElement("instruction");
        $insElem->setAttributeNode(new DOMAttr("order", strval($this->_instructionCount)));
        $insElem->setAttributeNode(new DOMAttr("opcode", strtoupper($instruction)));

        foreach ($operands as $index => $value) {
            $argElem = $this->_xml->createElement("arg" . ($index + 1));
            $operandSplit = $this->getTypeTuple($value);
            $argElem->setAttributeNode(new DOMAttr("type", $operandSplit["type"]));
            $argElem->appendChild(new DOMText($operandSplit["value"]));
            $insElem->appendChild($argElem);
        }

        $this->_root->appendChild($insElem);
    }

    /**
     * Splits and sets the input operand to type and value attributes.
     *
     * @param string $operand operand to split.
     * @return array array of split operand. ('type' => type, 'value' => value)
     */
    private function getTypeTuple($operand): array
    {
        $operandSplit = explode('@', $operand);

        $type = $operandSplit[0];
        $literalPattern = '%(int|bool|string|nil)%';
        if (!isset($operandSplit[1]))
            preg_match($literalPattern, $type) ? $type = "type" : $type = "label";
        else {
            if (!preg_match($literalPattern, $type)) {
                $type = "var";
                $operandSplit[1] = strtoupper($operandSplit[0]) . '@' . $operandSplit[1];
            }
        }

        return array(
            'type' => $type,
            'value' => isset($operandSplit[1]) ? $operandSplit[1] : $operandSplit[0]);
    }
}