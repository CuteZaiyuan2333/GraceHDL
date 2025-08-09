"""
GraceHDL语法分析器 - 新语法版本
支持新的GraceHDL语法特性：run语句、always语句、新数值格式等
"""

import ply.yacc as yacc
try:
    from .lexer import GraceHDLLexer
    from .ast_nodes import *
except ImportError:
    from lexer import GraceHDLLexer
    from ast_nodes import *

class GraceHDLParser:
    def __init__(self):
        self.lexer = GraceHDLLexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = None

    # 运算符优先级定义
    precedence = (
        ('left', 'LOR'),
        ('left', 'LAND'),
        ('left', 'OR'),
        ('left', 'XOR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE'),
        ('left', 'LT', 'LE', 'GT', 'GE'),
        ('left', 'PLUS', 'MINUS'),
        ('right', 'UMINUS', 'NOT'),
    )

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

    # 语法规则定义

    def p_source_text(self, p):
        '''source_text : source_items'''
        modules = [item for item in p[1] if isinstance(item, ModuleDeclaration)]
        p[0] = SourceText(modules, p[1])

    def p_source_items(self, p):
        '''source_items : source_items source_item
                       | source_item'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_source_item(self, p):
        '''source_item : module_declaration
                      | enum_declaration
                      | function_declaration
                      | testbench_declaration
                      | comment
                      | NEWLINE'''
        if p[1] in ['\n', None]:
            p[0] = None
        else:
            p[0] = p[1]

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
                      | NEWLINE INDENT module_body DEDENT
                      | empty'''
        if len(p) == 2:
            if p[1] is None:  # empty
                p[0] = []
            else:
                p[0] = [p[1]] if p[1] is not None else []
        elif len(p) == 3:  # module_body module_section
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]
        else:  # len(p) == 5, NEWLINE INDENT module_body DEDENT
            p[0] = p[3]

    def p_module_section(self, p):
        '''module_section : input_section
                         | output_section
                         | register_section
                         | parameter_section
                         | run_section
                         | always_section
                         | assign_section
                         | module_instantiation
                         | enum_declaration
                         | function_declaration
                         | interface_declaration
                         | generate_section
                         | comment
                         | NEWLINE'''
        if p[1] in ['\n', None]:
            p[0] = None
        else:
            p[0] = p[1]

    def p_comment(self, p):
        '''comment : COMMENT'''
        p[0] = CommentNode(p[1])

    def p_input_section(self, p):
        '''input_section : INPUT LPAREN port_list RPAREN
                        | INPUT LPAREN NEWLINE port_list RPAREN
                        | INPUT LPAREN NEWLINE INDENT port_list DEDENT RPAREN'''
        if len(p) == 5:
            p[0] = InputSection(p[3])
        elif len(p) == 6:
            p[0] = InputSection(p[4])
        else:  # len(p) == 7, with INDENT/DEDENT
            p[0] = InputSection(p[5])

    def p_output_section(self, p):
        '''output_section : OUTPUT LPAREN port_list RPAREN
                         | OUTPUT LPAREN NEWLINE port_list RPAREN
                         | OUTPUT LPAREN NEWLINE INDENT port_list DEDENT RPAREN'''
        if len(p) == 5:
            p[0] = OutputSection(p[3])
        elif len(p) == 6:
            p[0] = OutputSection(p[4])
        else:  # len(p) == 7, with INDENT/DEDENT
            p[0] = OutputSection(p[5])

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
        '''port_list : port_list port_item
                    | port_item'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_port_item(self, p):
        '''port_item : port_declaration
                    | comment
                    | NEWLINE'''
        if p[1] in ['\n', None]:
            p[0] = None
        else:
            p[0] = p[1]

    def p_port_declaration(self, p):
        '''port_declaration : net_type IDENTIFIER
                           | net_type IDENTIFIER COMMA
                           | net_type range_spec IDENTIFIER
                           | net_type range_spec IDENTIFIER COMMA'''
        if len(p) == 3:  # wire identifier
            p[0] = PortDeclaration('', p[1], None, [p[2]])
        elif len(p) == 4:
            if p[3] == ',':  # wire identifier,
                p[0] = PortDeclaration('', p[1], None, [p[2]])
            else:  # wire(7:0) identifier
                p[0] = PortDeclaration('', p[1], p[2], [p[3]])
        else:  # len(p) == 5, wire(7:0) identifier,
            p[0] = PortDeclaration('', p[1], p[2], [p[3]])

    def p_register_list(self, p):
        '''register_list : register_list register_item
                        | register_item'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_register_item(self, p):
        '''register_item : register_declaration
                        | comment
                        | NEWLINE'''
        if p[1] in ['\n', None]:
            p[0] = None
        else:
            p[0] = p[1]

    def p_register_declaration(self, p):
        '''register_declaration : REG IDENTIFIER
                               | REG IDENTIFIER COMMA
                               | REG range_spec IDENTIFIER
                               | REG range_spec IDENTIFIER COMMA
                               | REG IDENTIFIER LBRACKET expression COLON expression RBRACKET
                               | REG IDENTIFIER LBRACKET expression COLON expression RBRACKET COMMA
                               | REG range_spec IDENTIFIER LBRACKET expression COLON expression RBRACKET
                               | REG range_spec IDENTIFIER LBRACKET expression COLON expression RBRACKET COMMA'''
        if len(p) == 3:  # reg identifier
            p[0] = RegisterDeclaration(None, [p[2]])
        elif len(p) == 4 and p[3] == ',':  # reg identifier,
            p[0] = RegisterDeclaration(None, [p[2]])
        elif len(p) == 4:  # reg(7:0) identifier
            p[0] = RegisterDeclaration(p[2], [p[3]])
        elif len(p) == 5:  # reg(7:0) identifier,
            p[0] = RegisterDeclaration(p[2], [p[3]])
        elif len(p) == 8:  # reg identifier[msb:lsb]
            array_range = RangeSpec(p[4], p[6])
            p[0] = ArrayRegisterDeclaration(None, p[2], array_range)
        elif len(p) == 9 and p[8] == ',':  # reg identifier[msb:lsb],
            array_range = RangeSpec(p[4], p[6])
            p[0] = ArrayRegisterDeclaration(None, p[2], array_range)
        elif len(p) == 9:  # reg(7:0) identifier[msb:lsb]
            array_range = RangeSpec(p[5], p[7])
            p[0] = ArrayRegisterDeclaration(p[2], p[3], array_range)
        else:  # reg(7:0) identifier[msb:lsb],
            array_range = RangeSpec(p[5], p[7])
            p[0] = ArrayRegisterDeclaration(p[2], p[3], array_range)

    def p_parameter_list(self, p):
        '''parameter_list : parameter_list parameter_item
                         | parameter_item'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_parameter_item(self, p):
        '''parameter_item : parameter_declaration
                         | comment
                         | NEWLINE'''
        if p[1] in ['\n', None]:
            p[0] = None
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
        '''always_section : ALWAYS COLON statement_list
                          | ALWAYS COLON NEWLINE INDENT statement_list DEDENT'''
        if len(p) == 4:
            p[0] = AlwaysSection(p[3])
        else:
            p[0] = AlwaysSection(p[5])

    def p_assign_section(self, p):
        '''assign_section : ASSIGN COLON assign_statement_list
                         | ASSIGN COLON NEWLINE INDENT assign_statement_list DEDENT'''
        if len(p) == 4:
            p[0] = AssignSection(p[3])
        else:
            p[0] = AssignSection(p[5])

    def p_assign_statement_list(self, p):
        '''assign_statement_list : assign_statement_list assign_statement
                                | assign_statement'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_assign_statement(self, p):
        '''assign_statement : IDENTIFIER ASSIGN_OP expression
                           | IDENTIFIER LBRACKET expression RBRACKET ASSIGN_OP expression
                           | IDENTIFIER LBRACKET expression COLON expression RBRACKET ASSIGN_OP expression
                           | comment
                           | NEWLINE'''
        if p[1] in ['\n', None]:
            p[0] = None
        elif len(p) == 2:  # comment
            p[0] = p[1]
        elif len(p) == 4:  # identifier = expression
            p[0] = AssignmentStatement(p[1], p[3])
        elif len(p) == 7:  # identifier[index] = expression
            array_ref = IndexExpression(p[1], p[3])
            p[0] = AssignmentStatement(array_ref, p[6])
        else:  # identifier[msb:lsb] = expression
            array_ref = SliceExpression(p[1], p[3], p[5])
            p[0] = AssignmentStatement(array_ref, p[8])

    def p_clock_edge(self, p):
        '''clock_edge : POSEDGE IDENTIFIER
                     | NEGEDGE IDENTIFIER
                     | IDENTIFIER DOT POSEDGE
                     | IDENTIFIER DOT NEGEDGE'''
        if len(p) == 3:  # posedge clk
            p[0] = ClockEdge(p[2], p[1])
        else:  # clk.posedge
            p[0] = ClockEdge(p[1], p[3])

    def p_statement_list(self, p):
        '''statement_list : statement_list statement
                         | statement
                         | INDENT statement_list DEDENT'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        elif len(p) == 3:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]
        else:  # len(p) == 4, INDENT statement_list DEDENT
            p[0] = p[2]

    def p_statement(self, p):
        '''statement : assignment_statement
                    | if_statement
                    | case_statement
                    | for_statement
                    | return_statement
                    | assert_statement
                    | cover_statement
                    | wait_statement
                    | dump_waves_statement
                    | report_coverage_statement
                    | comment
                    | NEWLINE'''
        if p[1] == '\n':
            p[0] = None
        else:
            p[0] = p[1]

    def p_assignment_statement(self, p):
        '''assignment_statement : IDENTIFIER ASSIGN_OP expression
                                | IDENTIFIER LBRACKET expression RBRACKET ASSIGN_OP expression
                                | IDENTIFIER LBRACKET expression COLON expression RBRACKET ASSIGN_OP expression
                                | expression TO IDENTIFIER
                                | expression TO IDENTIFIER LBRACKET expression RBRACKET
                                | expression TO IDENTIFIER LBRACKET expression COLON expression RBRACKET'''
        if len(p) == 4:
            if p[2] == '=':  # 普通赋值: identifier = expression
                p[0] = AssignmentStatement(p[1], p[3])
            else:  # to 赋值: expression to identifier
                p[0] = ToAssignmentStatement(p[1], p[3])
        elif len(p) == 7:
            if p[5] == '=':  # 数组索引赋值: identifier[index] = expression
                array_ref = IndexExpression(p[1], p[3])
                p[0] = AssignmentStatement(array_ref, p[6])
            else:  # to 数组索引赋值: expression to identifier[index]
                array_ref = IndexExpression(p[3], p[5])
                p[0] = ToAssignmentStatement(p[1], array_ref)
        elif len(p) == 9:  # 数组切片赋值: identifier[msb:lsb] = expression
            array_ref = SliceExpression(p[1], p[3], p[5])
            p[0] = AssignmentStatement(array_ref, p[8])
        else:  # to 数组切片赋值: expression to identifier[msb:lsb]
            array_ref = SliceExpression(p[3], p[5], p[7])
            p[0] = ToAssignmentStatement(p[1], array_ref)

    def p_if_statement(self, p):
        '''if_statement : IF expression COLON statement_list
                       | IF expression COLON statement_list elif_list
                       | IF expression COLON statement_list ELSE COLON statement_list
                       | IF expression COLON statement_list elif_list ELSE COLON statement_list'''
        if len(p) == 5:
            p[0] = IfStatement(p[2], p[4], None, None)
        elif len(p) == 6:  # if with elif
            p[0] = IfStatement(p[2], p[4], None, p[5])
        elif len(p) == 8:  # if with else
            p[0] = IfStatement(p[2], p[4], p[7], None)
        else:  # if with elif and else
            p[0] = IfStatement(p[2], p[4], p[8], p[5])

    def p_elif_list(self, p):
        '''elif_list : elif_list elif_statement
                    | elif_statement'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_elif_statement(self, p):
        '''elif_statement : ELSIF expression COLON statement_list'''
        p[0] = ElifStatement(p[2], p[4])

    def p_case_statement(self, p):
        '''case_statement : CASE expression COLON case_item_list
                         | CASE expression COLON NEWLINE case_item_list
                         | CASE expression COLON NEWLINE INDENT case_item_list DEDENT'''
        if len(p) == 5:
            p[0] = CaseStatement(p[2], p[4])
        elif len(p) == 6:
            p[0] = CaseStatement(p[2], p[5])
        else:  # len(p) == 8
            p[0] = CaseStatement(p[2], p[6])

    def p_case_item_list(self, p):
        '''case_item_list : case_item_list case_item
                         | case_item_list NEWLINE case_item
                         | case_item'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        elif len(p) == 3:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]
        else:  # len(p) == 4, with NEWLINE
            if p[3] is not None:
                p[0] = p[1] + [p[3]]
            else:
                p[0] = p[1]

    def p_case_item(self, p):
        '''case_item : expression COLON statement_list
                    | DEFAULT COLON statement_list
                    | expression COLON NEWLINE INDENT statement_list DEDENT
                    | DEFAULT COLON NEWLINE INDENT statement_list DEDENT'''
        if len(p) == 4:
            if str(p[1]).lower() == 'default':
                p[0] = CaseItem(None, p[3])
            else:
                p[0] = CaseItem(p[1], p[3])
        else:  # len(p) == 7, with NEWLINE INDENT ... DEDENT
            if str(p[1]).lower() == 'default':
                p[0] = CaseItem(None, p[5])
            else:
                p[0] = CaseItem(p[1], p[5])

    def p_for_statement(self, p):
        '''for_statement : FOR IDENTIFIER IN range_expression COLON statement_list
                        | FOR IDENTIFIER IN range_expression COLON NEWLINE INDENT statement_list DEDENT'''
        if len(p) == 7:  # for i in range(...): statements
            p[0] = ForStatement(p[2], p[4], p[6])
        else:  # for i in range(...): NEWLINE INDENT statements DEDENT
            p[0] = ForStatement(p[2], p[4], p[8])

    def p_range_expression(self, p):
        '''range_expression : RANGE LPAREN expression COMMA expression RPAREN
                           | RANGE LPAREN expression COMMA expression COMMA expression RPAREN'''
        if len(p) == 7:  # range(start, end)
            p[0] = RangeExpression(p[3], p[5])
        else:  # range(start, end, step)
            p[0] = RangeExpression(p[3], p[5], p[7])

    def p_module_instantiation(self, p):
        '''module_instantiation : IDENTIFIER IDENTIFIER LPAREN port_connection_list RPAREN
                               | IDENTIFIER IDENTIFIER LPAREN RPAREN'''
        if len(p) == 6:  # 有端口连接
            p[0] = ModuleInstantiation(p[1], p[2], p[4])
        else:  # 无端口连接
            p[0] = ModuleInstantiation(p[1], p[2], [])

    def p_port_connection_list(self, p):
        '''port_connection_list : port_connection_list COMMA port_connection
                               | port_connection'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_port_connection(self, p):
        '''port_connection : DOT IDENTIFIER LPAREN IDENTIFIER RPAREN
                          | DOT IDENTIFIER LPAREN RPAREN'''
        if len(p) == 6:  # .port_name(signal_name)
            p[0] = PortConnection(p[2], p[4])
        else:  # .port_name() - 未连接
            p[0] = PortConnection(p[2], None)

    def p_net_type(self, p):
        '''net_type : WIRE
                   | REG'''
        p[0] = p[1]

    def p_range_spec(self, p):
        '''range_spec : LBRACKET expression COLON expression RBRACKET
                     | LPAREN expression COMMA expression RPAREN
                     | LPAREN expression COLON expression RPAREN'''
        # 支持方括号格式[msb:lsb]、新的逗号格式和旧的冒号格式（向后兼容）
        p[0] = RangeSpec(p[2], p[4])

    def p_expression(self, p):
        '''expression : expression PLUS expression
                     | expression MINUS expression
                     | expression LSHIFT expression
                     | expression RSHIFT expression
                     | expression AND expression
                     | expression OR expression
                     | expression XOR expression
                     | expression LAND expression
                     | expression LOR expression
                     | expression AND_KW expression
                     | expression OR_KW expression
                     | expression XOR_KW expression
                     | expression EQ expression
                     | expression NE expression
                     | expression LT expression
                     | expression LE expression
                     | expression GT expression
                     | expression GE expression
                     | NOT expression
                     | NOT_KW expression
                     | LNOT expression
                     | MINUS expression %prec UMINUS
                     | LPAREN expression RPAREN
                     | IDENTIFIER LBRACKET expression RBRACKET
                     | IDENTIFIER LBRACKET expression COLON expression RBRACKET
                     | IDENTIFIER
                     | NUMBER
                     | NEW_NUMBER_FORMAT
                     | BINARY_NUMBER
                     | HEX_NUMBER
                     | enum_reference
                     | function_call
                     | reduce_operation'''
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
        elif len(p) == 3:  # 一元运算符
            operator = p[1]
            # 将关键字形式的一元运算符映射到符号形式
            if operator == 'not':
                operator = '~'
            p[0] = UnaryExpression(operator, p[2])
        elif len(p) == 4 and p[1] == '(':
            p[0] = p[2]
        elif len(p) == 5:  # 数组索引: IDENTIFIER[expression]
            p[0] = IndexExpression(p[1], p[3])
        elif len(p) == 7:  # 数组切片: IDENTIFIER[expression:expression]
            p[0] = SliceExpression(p[1], p[3], p[5])
        else:
            operator = p[2]
            # 将关键字形式的二元运算符映射到符号形式
            if operator == 'and':
                operator = '&'
            elif operator == 'or':
                operator = '|'
            elif operator == 'xor':
                operator = '^'
            p[0] = BinaryExpression(operator, p[1], p[3])

    # 枚举类型语法规则
    def p_enum_declaration(self, p):
        '''enum_declaration : ENUM IDENTIFIER COLON NEWLINE enum_item_list'''
        p[0] = EnumDeclaration(p[2], p[5])

    def p_enum_item_list(self, p):
        '''enum_item_list : enum_item_list NEWLINE enum_item
                         | enum_item_list enum_item
                         | enum_item'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        elif len(p) == 3:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]
        else:  # len(p) == 4, with NEWLINE
            if p[3] is not None:
                p[0] = p[1] + [p[3]]
            else:
                p[0] = p[1]
        
        # 过滤掉None项
        if isinstance(p[0], list):
            p[0] = [item for item in p[0] if item is not None]

    def p_enum_item(self, p):
        '''enum_item : IDENTIFIER ASSIGN_OP expression
                    | IDENTIFIER
                    | NEWLINE'''
        if len(p) == 2:
            if p[1] == '\n':
                p[0] = None
            else:
                p[0] = EnumItem(p[1])
        else:
            p[0] = EnumItem(p[1], p[3])

    # 函数定义语法规则
    def p_function_declaration(self, p):
        '''function_declaration : DEF IDENTIFIER LPAREN parameter_name_list RPAREN COLON statement_list
                               | DEF IDENTIFIER LPAREN RPAREN COLON statement_list
                               | DEF IDENTIFIER LPAREN parameter_name_list RPAREN COLON NEWLINE INDENT statement_list DEDENT
                               | DEF IDENTIFIER LPAREN RPAREN COLON NEWLINE INDENT statement_list DEDENT'''
        if len(p) == 8:  # 有参数，无缩进
            p[0] = FunctionDeclaration(p[2], p[4], p[7])
        elif len(p) == 7:  # 无参数，无缩进
            p[0] = FunctionDeclaration(p[2], [], p[6])
        elif len(p) == 11:  # 有参数，有缩进
            p[0] = FunctionDeclaration(p[2], p[4], p[9])
        else:  # 无参数，有缩进
            p[0] = FunctionDeclaration(p[2], [], p[8])

    def p_parameter_name_list(self, p):
        '''parameter_name_list : parameter_name_list COMMA IDENTIFIER
                              | IDENTIFIER'''
        if len(p) == 2:
            p[0] = [FunctionParameter(p[1])]
        else:
            p[0] = p[1] + [FunctionParameter(p[3])]

    def p_return_statement(self, p):
        '''return_statement : RETURN expression'''
        p[0] = ReturnStatement(p[2])

    # 接口定义语法规则
    def p_interface_declaration(self, p):
        '''interface_declaration : INTERFACE IDENTIFIER COLON interface_body
                                | INTERFACE IDENTIFIER COLON NEWLINE interface_body'''
        if len(p) == 5:
            p[0] = InterfaceDeclaration(p[2], [], p[4])
        else:
            p[0] = InterfaceDeclaration(p[2], [], p[5])

    def p_interface_body(self, p):
        '''interface_body : interface_body interface_section
                         | interface_section'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_interface_section(self, p):
        '''interface_section : parameter_section
                            | input_section
                            | output_section
                            | comment
                            | NEWLINE'''
        if p[1] in ['\n', None]:
            p[0] = None
        else:
            p[0] = p[1]

    # 生成语句语法规则
    def p_generate_section(self, p):
        '''generate_section : GENERATE COLON generate_statement_list
                           | GENERATE COLON NEWLINE INDENT generate_statement_list DEDENT'''
        if len(p) == 4:
            p[0] = GenerateSection(p[3])
        else:
            p[0] = GenerateSection(p[5])

    def p_generate_statement_list(self, p):
        '''generate_statement_list : generate_statement_list generate_statement
                                  | generate_statement'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_generate_statement(self, p):
        '''generate_statement : for_generate_statement
                             | module_instantiation
                             | comment
                             | NEWLINE'''
        if p[1] in ['\n', None]:
            p[0] = None
        else:
            p[0] = p[1]

    def p_for_generate_statement(self, p):
        '''for_generate_statement : FOR IDENTIFIER IN function_call COLON generate_statement_list
                                 | FOR IDENTIFIER IN function_call COLON NEWLINE INDENT generate_statement_list DEDENT'''
        # 假设是range(start, end)或range(end)的调用
        range_call = p[4]
        if len(range_call.arguments) == 1:
            start, end, step = 0, range_call.arguments[0], 1
        elif len(range_call.arguments) == 2:
            start, end, step = range_call.arguments[0], range_call.arguments[1], 1
        else:
            start, end, step = range_call.arguments[0], range_call.arguments[1], range_call.arguments[2]
        
        if len(p) == 7:
            p[0] = ForGenerateStatement(p[2], start, end, step, p[6])
        else:
            p[0] = ForGenerateStatement(p[2], start, end, step, p[8])

    # 断言语法规则
    def p_assert_statement(self, p):
        '''assert_statement : ASSERT LPAREN expression COMMA STRING RPAREN
                           | ASSERT LPAREN expression RPAREN'''
        if len(p) == 7:
            p[0] = AssertStatement(p[3], p[5])
        else:
            p[0] = AssertStatement(p[3])

    def p_cover_statement(self, p):
        '''cover_statement : COVER LPAREN expression COMMA STRING RPAREN
                          | COVER LPAREN expression RPAREN'''
        if len(p) == 7:
            p[0] = CoverStatement(p[3], p[5])
        else:
            p[0] = CoverStatement(p[3])

    # 归约运算符语法规则
    def p_reduce_operation(self, p):
        '''reduce_operation : REDUCE_AND LPAREN expression RPAREN
                           | REDUCE_OR LPAREN expression RPAREN
                           | REDUCE_XOR LPAREN expression RPAREN'''
        operator = p[1].split('_')[1].lower()  # 从 'reduce_and' 提取 'and'
        p[0] = ReduceOperation(operator, p[3])

    # 枚举引用语法规则
    def p_enum_reference(self, p):
        '''enum_reference : IDENTIFIER DOT IDENTIFIER'''
        p[0] = EnumReference(p[1], p[3])

    # 函数调用语法规则
    def p_function_call(self, p):
        '''function_call : IDENTIFIER LPAREN argument_list RPAREN
                        | IDENTIFIER LPAREN RPAREN'''
        if len(p) == 5:
            p[0] = FunctionCall(p[1], p[3])
        else:
            p[0] = FunctionCall(p[1], [])

    def p_argument_list(self, p):
        '''argument_list : argument_list COMMA expression
                        | expression'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    # 测试台语法规则
    def p_testbench_declaration(self, p):
        '''testbench_declaration : TESTBENCH FOR IDENTIFIER COLON testbench_body
                                | TESTBENCH FOR IDENTIFIER COLON NEWLINE testbench_body'''
        if len(p) == 6:
            p[0] = TestbenchDeclaration(p[3], [], p[5])
        else:
            p[0] = TestbenchDeclaration(p[3], [], p[6])

    def p_testbench_body(self, p):
        '''testbench_body : testbench_body testbench_section
                         | testbench_section'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_testbench_section(self, p):
        '''testbench_section : parameter_section
                            | clock_declaration
                            | signal_declaration
                            | dut_instantiation
                            | test_sequence
                            | dump_waves_statement
                            | report_coverage_statement
                            | comment
                            | NEWLINE'''
        if p[1] in ['\n', None]:
            p[0] = None
        else:
            p[0] = p[1]

    def p_clock_declaration(self, p):
        '''clock_declaration : CLOCK IDENTIFIER WITH PERIOD expression'''
        p[0] = ClockDeclaration(p[2], p[5])

    def p_signal_declaration(self, p):
        '''signal_declaration : SIGNAL IDENTIFIER COLON net_type ASSIGN_OP expression
                             | SIGNAL IDENTIFIER COLON net_type range_spec ASSIGN_OP expression
                             | SIGNAL IDENTIFIER COLON net_type
                             | SIGNAL IDENTIFIER COLON net_type range_spec'''
        if len(p) == 7:  # signal name: wire = value
            p[0] = SignalDeclaration(p[2], p[4], None, p[6])
        elif len(p) == 8:  # signal name: wire(7:0) = value
            p[0] = SignalDeclaration(p[2], p[4], p[5], p[7])
        elif len(p) == 5:  # signal name: wire
            p[0] = SignalDeclaration(p[2], p[4], None, None)
        else:  # signal name: wire(7:0)
            p[0] = SignalDeclaration(p[2], p[4], p[5], None)

    def p_dut_instantiation(self, p):
        '''dut_instantiation : IDENTIFIER COLON IDENTIFIER LPAREN parameter_assignments RPAREN port_connections
                            | IDENTIFIER COLON IDENTIFIER LPAREN RPAREN port_connections
                            | IDENTIFIER COLON IDENTIFIER port_connections'''
        if len(p) == 8:  # dut: module(params) connections
            p[0] = DutInstantiation(p[1], p[3], p[5], p[7])
        elif len(p) == 7:  # dut: module() connections
            p[0] = DutInstantiation(p[1], p[3], [], p[6])
        else:  # dut: module connections
            p[0] = DutInstantiation(p[1], p[3], [], p[4])

    def p_parameter_assignments(self, p):
        '''parameter_assignments : parameter_assignments COMMA parameter_assignment
                                | parameter_assignment'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_parameter_assignment(self, p):
        '''parameter_assignment : IDENTIFIER ASSIGN_OP expression'''
        p[0] = ParameterAssignment(p[1], p[3])

    def p_port_connections(self, p):
        '''port_connections : port_connections port_connection
                           | port_connection'''
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            if p[2] is not None:
                p[0] = p[1] + [p[2]]
            else:
                p[0] = p[1]

    def p_port_connection(self, p):
        '''port_connection : DOT IDENTIFIER LPAREN IDENTIFIER RPAREN
                          | NEWLINE'''
        if len(p) == 6:  # .port(signal)
            p[0] = PortConnection(p[2], p[4])
        else:
            p[0] = None

    def p_test_sequence(self, p):
        '''test_sequence : IDENTIFIER COLON statement_list
                        | IDENTIFIER COLON NEWLINE INDENT statement_list DEDENT'''
        if len(p) == 4:
            p[0] = TestSequence(p[3])
        else:
            p[0] = TestSequence(p[5])

    def p_wait_statement(self, p):
        '''wait_statement : WAIT FOR expression'''
        p[0] = WaitStatement(p[3])

    def p_dump_waves_statement(self, p):
        '''dump_waves_statement : DUMP_WAVES TO STRING'''
        p[0] = DumpWavesStatement(p[3])

    def p_report_coverage_statement(self, p):
        '''report_coverage_statement : REPORT_COVERAGE'''
        p[0] = ReportCoverageStatement()

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
        if not hasattr(self, 'parser') or self.parser is None:
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