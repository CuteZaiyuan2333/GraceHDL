"""
GraceHDL词法分析器
使用PLY库实现词法分析
"""

import ply.lex as lex

class GraceHDLLexer:
    # 保留字
    reserved = {
        'module': 'MODULE',
        'endmodule': 'ENDMODULE',
        'input': 'INPUT',
        'output': 'OUTPUT',
        'inout': 'INOUT',
        'wire': 'WIRE',
        'reg': 'REG',
        'assign': 'ASSIGN',
        'always': 'ALWAYS',
        'run': 'RUN',
        'register': 'REGISTER',
        'parameter': 'PARAMETER',
        'if': 'IF',
        'else': 'ELSE',
        'elsif': 'ELSIF',
        'case': 'CASE',
        'default': 'DEFAULT',
        'for': 'FOR',
        'while': 'WHILE',
        'posedge': 'POSEDGE',
        'negedge': 'NEGEDGE',
        'localparam': 'LOCALPARAM',
        'function': 'FUNCTION',
        'task': 'TASK',
        'begin': 'BEGIN',
        'end': 'END',
        'initial': 'INITIAL',
    }

    # 标记列表
    tokens = [
        'IDENTIFIER',
        'NUMBER',
        'BINARY_NUMBER',
        'HEX_NUMBER',
        'OCTAL_NUMBER',
        'NEW_NUMBER_FORMAT',  # 新的数值格式 (value, base, width)
        'STRING',
        'COMMENT',
        
        # 运算符
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
        'ASSIGN_OP', 'ASSIGN_NB',
        'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
        'AND', 'OR', 'NOT', 'XOR', 'NAND', 'NOR', 'XNOR',
        'LAND', 'LOR', 'LNOT',
        'LSHIFT', 'RSHIFT',
        
        # 分隔符
        'LPAREN', 'RPAREN',
        'LBRACKET', 'RBRACKET',
        'LBRACE', 'RBRACE',
        'COMMA', 'SEMICOLON', 'COLON',
        'DOT', 'QUESTION',
        
        # 特殊标记
        'NEWLINE', 'INDENT', 'DEDENT',
        'AT', 'HASH',
    ] + list(reserved.values())

    # 简单标记
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MODULO = r'%'
    t_ASSIGN_OP = r'='
    t_ASSIGN_NB = r'<='
    t_EQ = r'=='
    t_NE = r'!='
    t_LT = r'<'
    t_LE = r'<='
    t_GT = r'>'
    t_GE = r'>='
    t_AND = r'&'
    t_OR = r'\|'
    t_NOT = r'~'
    t_XOR = r'\^'
    t_NAND = r'~&'
    t_NOR = r'~\|'
    t_XNOR = r'~\^'
    t_LAND = r'&&'
    t_LOR = r'\|\|'
    t_LNOT = r'!'
    t_LSHIFT = r'<<'
    t_RSHIFT = r'>>'
    
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_COLON = r':'
    t_DOT = r'\.'
    t_QUESTION = r'\?'
    t_AT = r'@'
    t_HASH = r'\#'

    # 忽略空格和制表符（但不忽略换行符）
    t_ignore = ' \t'

    def __init__(self):
        self.lexer = None
        self.indent_stack = [0]  # 缩进栈
        self.at_line_start = True
        self.paren_level = 0
        self.pending_dedents = 0  # 待处理的DEDENT数量

    def t_COMMENT_SINGLE(self, t):
        r'//.*'
        pass  # 忽略单行注释
    
    def t_COMMENT_MULTI(self, t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')
        pass  # 忽略多行注释

    def t_NEW_NUMBER_FORMAT(self, t):
        r'\(\s*[0-9a-fA-F]+\s*,\s*[dbho]\s*,\s*\d+\s*\)'  # 支持各种进制的数字格式
        # 解析新的数值格式
        content = t.value[1:-1]  # 去掉括号
        parts = [part.strip() for part in content.split(',')]
        if len(parts) == 3:
            try:
                value_str, base_str, width_str = parts
                # 解析数值
                if base_str == 'd':
                    value = int(value_str, 10)
                elif base_str == 'b':
                    value = int(value_str, 2)
                elif base_str == 'h':
                    value = int(value_str, 16)
                elif base_str == 'o':
                    value = int(value_str, 8)
                else:
                    value = int(value_str, 10)
                
                width = int(width_str)
                t.value = (value, base_str, width)
                return t
            except ValueError:
                pass
        # 如果解析失败，当作普通的括号处理
        return None

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    def t_HEX_NUMBER(self, t):
        r"[0-9]*'h[0-9a-fA-F_]+"
        return t

    def t_BINARY_NUMBER(self, t):
        r"[0-9]*'b[01_]+"
        return t

    def t_OCTAL_NUMBER(self, t):
        r"[0-9]*'o[0-7_]+"
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'"([^"\\]|\\.)*"'
        return t

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        self.at_line_start = True
        return t  # 总是返回换行符，让语法分析器决定如何处理

    def t_error(self, t):
        print(f"非法字符 '{t.value[0]}' 在行 {t.lineno}")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer
    
    def input(self, data):
        """设置输入数据"""
        self.lexer.input(data)
        # 重置状态
        self.indent_stack = [0]
        self.at_line_start = True
        self.paren_level = 0
        self.pending_dedents = 0

    def token(self):
        """简化的token方法，不处理缩进"""
        return self.lexer.token()

    def handle_indentation(self):
        """处理缩进逻辑"""
        # 计算当前行的缩进级别
        indent_level = 0
        pos = self.lexer.lexpos
        
        # 跳过当前位置的空白字符来计算缩进
        while pos < len(self.lexer.lexdata) and self.lexer.lexdata[pos] in ' \t':
            if self.lexer.lexdata[pos] == ' ':
                indent_level += 1
            elif self.lexer.lexdata[pos] == '\t':
                indent_level += 8  # 制表符等于8个空格
            pos += 1

        # 如果是空行或注释行，跳过缩进处理
        if pos >= len(self.lexer.lexdata) or self.lexer.lexdata[pos] in '\n/':
            return None  # 不返回缩进标记，继续正常处理

        current_indent = self.indent_stack[-1]
        
        if indent_level > current_indent:
            # 缩进增加
            self.indent_stack.append(indent_level)
            # 跳过空白字符
            self.lexer.lexpos = pos
            tok = lex.LexToken()
            tok.type = 'INDENT'
            tok.value = None
            tok.lineno = self.lexer.lineno
            tok.lexpos = self.lexer.lexpos
            return tok
        elif indent_level < current_indent:
            # 缩进减少，可能需要多个DEDENT
            dedent_count = 0
            while self.indent_stack and self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                dedent_count += 1
            
            if dedent_count > 0:
                # 跳过空白字符
                self.lexer.lexpos = pos
                tok = lex.LexToken()
                tok.type = 'DEDENT'
                tok.value = None
                tok.lineno = self.lexer.lineno
                tok.lexpos = self.lexer.lexpos
                # 设置待处理的DEDENT数量
                self.pending_dedents = dedent_count - 1
                return tok
        else:
            # 缩进级别相同，跳过空白字符
            self.lexer.lexpos = pos
        
        # 缩进级别相同，不返回缩进标记
        return None

if __name__ == "__main__":
    # 测试词法分析器
    lexer = GraceHDLLexer()
    lexer.build()
    
    test_code = """
module test_module
    input wire clk, reset
    output reg[7:0] counter
    
    always @(posedge clk)
        if reset
            counter <= 8'b0
        else
            counter <= counter + 1
"""
    
    lexer.lexer.input(test_code)
    
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"{tok.type}: {tok.value}")