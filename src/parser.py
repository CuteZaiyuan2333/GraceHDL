"""
GraceHDL语法分析器 - 新语法版本
支持新的GraceHDL语法特性：run语句、always语句、新数值格式等
"""

import ply.yacc as yacc
from .lexer import GraceHDLLexer
from .ast_nodes import *

class GraceHDLParser:
    def __init__(self):
        self.lexer = GraceHDLLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = None

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

    # 语法规则定义

    def p_source_text(self, p):
        '''source_text : module_declaration'''
        p[0] = SourceText([p[1]])

    def p_module_declaration(self, p):
        '''module_declaration : MODULE IDENTIFIER COLON module_body
                             | MODULE IDENTIFIER COLON NEWLINE module_body'''
        if len(p) == 5:
            p[0] = ModuleDeclaration(p[2], [], [], p[4])
        else:
            p[0] = ModuleDeclaration(p[2], [], [], p[5])

    def p_module_body(self, p):
        '''module_body : module_body module_section
                      | module_section
                      | empty'''
        if len(p) == 2:
            if p[1] is None:  # empty
                p[0] = []
            else:
                p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_module_section(self, p):
        '''module_section : input_section
                         | output_section
                         | register_section
                         | parameter_section
                         | run_section
                         | always_section
                         | NEWLINE'''
        if p[1] in ['\n', None]:
            p[0] = None
        else:
            p[0] = p[1]

    def p_input_section(self, p):
        '''input_section : INPUT LPAREN port_list RPAREN
                        | INPUT LPAREN NEWLINE port_list RPAREN'''
        if len(p) == 5:
            p[0] = InputSection(p[3])
        else:
            p[0] = InputSection(p[4])

    def p_output_section(self, p):
        '''output_section : OUTPUT LPAREN port_list RPAREN
                         | OUTPUT LPAREN NEWLINE port_list RPAREN'''
        if len(p) == 5:
            p[0] = OutputSection(p[3])
        else:
            p[0] = OutputSection(p[4])

    def p_register_section(self, p):
        '''register_section : REGISTER LPAREN register_list RPAREN
                           | REGISTER LPAREN NEWLINE register_list RPAREN'''
        if len(p) == 5:
            p[0] = RegisterSection(p[3])
        else:
            p[0] = RegisterSection(p[4])

    def p_parameter_section(self, p):
        '''parameter_section : PARAMETER LPAREN parameter_list RPAREN
                            | PARAMETER LPAREN NEWLINE parameter_list RPAREN'''
        if len(p) == 5:
            p[0] = ParameterSection(p[3])
        else:
            p[0] = ParameterSection(p[4])

    def p_port_list(self, p):
        '''port_list : port_list port_declaration
                    | port_declaration'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_port_declaration(self, p):
        '''port_declaration : net_type IDENTIFIER
                           | net_type IDENTIFIER COMMA
                           | net_type range_spec IDENTIFIER
                           | net_type range_spec IDENTIFIER COMMA'''
        if len(p) == 3:  # wire identifier
            p[0] = PortDeclaration('', p[1], None, [p[2]])
        elif len(p) == 4 and p[3] == ',':  # wire identifier,
            p[0] = PortDeclaration('', p[1], None, [p[2]])
        elif len(p) == 4:  # wire(7:0) identifier
            p[0] = PortDeclaration('', p[1], p[2], [p[3]])
        else:  # wire(7:0) identifier,
            p[0] = PortDeclaration('', p[1], p[2], [p[3]])

    def p_register_list(self, p):
        '''register_list : register_list register_declaration
                        | register_declaration'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_register_declaration(self, p):
        '''register_declaration : REG IDENTIFIER
                               | REG IDENTIFIER COMMA
                               | REG range_spec IDENTIFIER
                               | REG range_spec IDENTIFIER COMMA'''
        if len(p) == 3:  # reg identifier
            p[0] = RegisterDeclaration(None, [p[2]])
        elif len(p) == 4 and p[3] == ',':  # reg identifier,
            p[0] = RegisterDeclaration(None, [p[2]])
        elif len(p) == 4:  # reg(7:0) identifier
            p[0] = RegisterDeclaration(p[2], [p[3]])
        else:  # reg(7:0) identifier,
            p[0] = RegisterDeclaration(p[2], [p[3]])

    def p_parameter_list(self, p):
        '''parameter_list : parameter_list parameter_declaration
                         | parameter_declaration'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_parameter_declaration(self, p):
        '''parameter_declaration : IDENTIFIER ASSIGN_OP expression
                                | IDENTIFIER ASSIGN_OP expression COMMA'''
        p[0] = ParameterDeclaration(p[1], p[3])

    def p_run_section(self, p):
        '''run_section : RUN LPAREN clock_edge RPAREN COLON statement_list'''
        p[0] = RunSection(p[3], p[6])

    def p_always_section(self, p):
        '''always_section : ALWAYS COLON statement_list'''
        p[0] = AlwaysSection(p[3])

    def p_clock_edge(self, p):
        '''clock_edge : IDENTIFIER DOT POSEDGE
                     | IDENTIFIER DOT NEGEDGE'''
        p[0] = ClockEdge(p[1], p[3])

    def p_statement_list(self, p):
        '''statement_list : statement_list statement
                         | statement'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_statement(self, p):
        '''statement : assignment_statement
                    | if_statement
                    | case_statement
                    | NEWLINE'''
        if p[1] == '\n':
            p[0] = None
        else:
            p[0] = p[1]

    def p_assignment_statement(self, p):
        '''assignment_statement : IDENTIFIER ASSIGN_OP expression'''
        p[0] = AssignmentStatement(p[1], p[3])

    def p_if_statement(self, p):
        '''if_statement : IF expression COLON statement_list
                       | IF expression COLON statement_list ELSE COLON statement_list'''
        if len(p) == 5:
            p[0] = IfStatement(p[2], p[4], None)
        else:
            p[0] = IfStatement(p[2], p[4], p[7])

    def p_case_statement(self, p):
        '''case_statement : CASE expression COLON case_item_list
                         | CASE expression COLON NEWLINE case_item_list'''
        if len(p) == 5:
            p[0] = CaseStatement(p[2], p[4])
        else:
            p[0] = CaseStatement(p[2], p[5])

    def p_case_item_list(self, p):
        '''case_item_list : case_item_list case_item
                         | case_item_list NEWLINE case_item
                         | case_item'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 3:
            p[0] = p[1] + [p[2]]
        else:  # len(p) == 4, with NEWLINE
            p[0] = p[1] + [p[3]]

    def p_case_item(self, p):
        '''case_item : expression COLON statement_list
                    | DEFAULT COLON statement_list'''
        if len(p) == 4 and str(p[1]).lower() == 'default':
            p[0] = CaseItem(None, p[3])
        else:
            p[0] = CaseItem(p[1], p[3])

    def p_net_type(self, p):
        '''net_type : WIRE
                   | REG'''
        p[0] = p[1]

    def p_range_spec(self, p):
        '''range_spec : LPAREN expression COLON expression RPAREN'''
        p[0] = RangeSpec(p[2], p[4])

    def p_expression(self, p):
        '''expression : expression PLUS expression
                     | expression MINUS expression
                     | expression AND expression
                     | expression OR expression
                     | expression XOR expression
                     | expression EQ expression
                     | expression NE expression
                     | expression LT expression
                     | expression LE expression
                     | expression GT expression
                     | expression GE expression
                     | LPAREN expression RPAREN
                     | IDENTIFIER
                     | NUMBER
                     | NEW_NUMBER_FORMAT
                     | BINARY_NUMBER
                     | HEX_NUMBER'''
        if len(p) == 2:
            if isinstance(p[1], str):
                if p[1].isdigit():
                    p[0] = NumberExpression(int(p[1]))
                elif "'" in p[1]:
                    p[0] = NumberExpression(p[1])
                else:
                    p[0] = IdentifierExpression(p[1])
            elif isinstance(p[1], tuple):  # NEW_NUMBER_FORMAT
                value, base, width = p[1]
                p[0] = NewNumberExpression(value, base, width)
            else:
                p[0] = p[1]
        elif len(p) == 4 and p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = BinaryExpression(p[2], p[1], p[3])

    def p_empty(self, p):
        '''empty :'''
        p[0] = None

    def p_error(self, p):
        if p:
            print(f"语法错误在标记 {p.type} ('{p.value}') 行 {p.lineno}")
        else:
            print("语法错误：意外的文件结束")

    def build(self, **kwargs):
        """构建语法分析器"""
        self.lexer = GraceHDLLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
    
    def parse(self, source_code):
        """解析源代码"""
        if not hasattr(self, 'parser'):
            self.build()
        return self.parser.parse(source_code, lexer=self.lexer.lexer)

if __name__ == "__main__":
    parser = GraceHDLParser()
    parser.build()
    
    test_code = """module test_counter:
    input(
        wire clk,
        wire rst
    )
    output(
        wire(7:0) count
    )
    register(
        reg(7:0) count_reg
    )
    
    run (clk.posedge):
        if rst:
            count_reg = (0, d, 8)
        else:
            count_reg = count_reg + (1, d, 8)
    
    always:
        count = count_reg
"""
    
    result = parser.parser.parse(test_code, lexer=parser.lexer)
    print("解析成功！")
    print(result)