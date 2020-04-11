class Patterns:
    """ Types """

    @property
    def var_type(self):
        return r'^(?:var)$'

    @property
    def int_type(self):
        return r'^(?:int)$'

    @property
    def bool_type(self):
        return r'^(?:bool)$'

    @property
    def string_type(self):
        return r'^(?:string)$'

    @property
    def nil_type(self):
        return r'^(?:nil)$'

    @property
    def label_type(self):
        return r'^(?:label)$'

    @property
    def type_type(self):
        return r'^(?:type)$'

    @property
    def const_type(self):
        return r'(?:' + self.nil_type + '|' + self.bool_type + '|' + self.int_type + '|' + self.string_type + ')'

    @property
    def symbol_type(self):
        return r'^(?:' + self.var_type + '|(' + self.const_type + '))$'

    """ Values """

    @property
    def identifier_special_chars(self):
        return r'_\-\$\&\%\*\!\?'

    @property
    def identifier(self):
        return r'(?:[a-zA-Z' + self.identifier_special_chars + '][\w' + self.identifier_special_chars + ']*)'

    @property
    def var_val(self):
        return r'^(GF|LF|TF)@' + '(' + self.identifier + ')$'

    @property
    def nil_val(self):
        return r'(?:nil)'

    @property
    def bool_val(self):
        return r'(?:true|false)'

    @property
    def int_val(self):
        return r'(?:-?|\+?)\d+'

    @property
    def string_val(self):
        return r'(?:[^\s#\\]|(?:\\\d{3}))*'

    @property
    def const_val(self):
        return r'((?:' + self.nil_val + '|' + self.bool_val + '|' + self.int_val + '|' + self.string_val + '))'

    @property
    def label_val(self):
        return r'^(' + self.identifier + ')$'

    @property
    def symbol_val(self):
        return r'^(?:' + self.var_val + '|' + self.const_val + ')$'

    @property
    def type_val(self):
        return r'^(' + self.int_val + '|' + self.string_val + '|' + self.bool_val + ')$'
