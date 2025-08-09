"""
Verilog代码生成器 - 新语法版本
将GraceHDL的AST转换为标准Verilog HDL代码
支持新的数值格式和run/always语句
"""

from .ast_nodes import *

class VerilogGenerator:
    """Verilog代码生成器"""
    
    def __init__(self):
        self.indent_level = 0
        self.output = []

    def generate(self, ast):
        """生成Verilog代码"""
        self.output = []
        self.indent_level = 0
        self.visit(ast)
        return '\n'.join(self.output)

    def emit(self, code):
        """输出一行代码"""
        indent = '    ' * self.indent_level
        self.output.append(indent + code)

    def visit(self, node):
        """访问AST节点"""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """通用访问方法"""
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_NoneType(self, node):
        """处理None值"""
        return ""

    def visit_SourceText(self, node):
        """访问源代码根节点"""
        for module in node.modules:
            self.visit(module)
            self.emit('')  # 模块间空行

    def visit_ModuleDeclaration(self, node):
        """访问模块声明"""
        # 模块头
        module_header = f'module {node.name}'
        
        # 参数列表
        if node.parameters:
            param_list = []
            for param in node.parameters:
                param_str = f'parameter {param.name} = {self.visit_expression(param.value)}'
                param_list.append(param_str)
            module_header += f' #({", ".join(param_list)})'
        
        # 端口列表
        if node.ports:
            port_list = []
            for port in node.ports:
                port_str = self.format_port_declaration(port)
                port_list.append(port_str)
            module_header += f'({", ".join(port_list)})'
        
        self.emit(module_header + ';')
        self.emit('')
        
        # 模块内容
        self.indent_level += 1
        for section in node.sections:
            self.visit(section)
            self.emit('')  # 段落间空行
        self.indent_level -= 1
        
        self.emit('endmodule')

    def format_port_declaration(self, port):
        """格式化端口声明"""
        result = f'{port.direction} {port.net_type}'
        if port.range_spec:
            result += f'[{self.visit_expression(port.range_spec.msb)}:{self.visit_expression(port.range_spec.lsb)}]'
        result += f' {", ".join(port.names)}'
        return result

    # 新语法节点访问方法

    def visit_InputSection(self, node):
        """访问输入端口段"""
        for port in node.ports:
            self.visit(port)

    def visit_OutputSection(self, node):
        """访问输出端口段"""
        for port in node.ports:
            self.visit(port)

    def visit_RegisterSection(self, node):
        """访问寄存器段"""
        for register in node.registers:
            self.visit(register)

    def visit_ParameterSection(self, node):
        """访问参数段"""
        for parameter in node.parameters:
            self.visit(parameter)

    def visit_RunSection(self, node):
        """访问run语句段（时序逻辑）"""
        # 转换为always块
        always_str = f'always @({self.visit_clock_edge(node.clock_edge)})'
        self.emit(always_str)
        self.emit('begin')
        self.indent_level += 1
        for stmt in node.statements:
            self.visit(stmt)
        self.indent_level -= 1
        self.emit('end')

    def visit_AlwaysSection(self, node):
        """访问always语句段（组合逻辑）"""
        # 转换为always_comb块
        self.emit('always_comb')
        self.emit('begin')
        self.indent_level += 1
        for stmt in node.statements:
            self.visit(stmt)
        self.indent_level -= 1
        self.emit('end')

    def visit_ClockEdge(self, node):
        """访问时钟边沿"""
        return f'{node.edge_type} {self.visit_expression(node.signal)}'

    def visit_clock_edge(self, node):
        """访问时钟边沿（内部方法）"""
        return f'{node.edge_type} {self.visit_expression(node.signal)}'

    def visit_PortDeclaration(self, node):
        """访问端口声明"""
        port_str = self.format_port_declaration(node)
        self.emit(port_str + ';')

    def visit_RegisterDeclaration(self, node):
        """访问寄存器声明"""
        reg_str = 'reg'
        if node.range_spec:
            reg_str += f'[{self.visit_expression(node.range_spec.msb)}:{self.visit_expression(node.range_spec.lsb)}]'
        reg_str += f' {", ".join(node.names)}'
        self.emit(reg_str + ';')

    def visit_ParameterDeclaration(self, node):
        """访问参数声明"""
        param_str = f'parameter {node.name} = {self.visit_expression(node.value)}'
        self.emit(param_str + ';')

    def visit_AssignmentStatement(self, node):
        """访问赋值语句"""
        # 在run块中使用非阻塞赋值，在always块中使用阻塞赋值
        assign_str = f'{self.visit_expression(node.target)} = {self.visit_expression(node.expression)}'
        self.emit(assign_str + ';')

    # 兼容性方法

    def visit_NetDeclaration(self, node):
        """访问网络声明"""
        net_str = node.net_type
        if node.range_spec:
            net_str += f'[{self.visit_expression(node.range_spec.msb)}:{self.visit_expression(node.range_spec.lsb)}]'
        net_str += f' {", ".join(node.names)}'
        self.emit(net_str + ';')

    def visit_ContinuousAssign(self, node):
        """访问连续赋值"""
        for assignment in node.assignments:
            assign_str = f'assign {self.visit_expression(assignment.lvalue)} = {self.visit_expression(assignment.rvalue)}'
            self.emit(assign_str + ';')

    def visit_AlwaysConstruct(self, node):
        """访问always块"""
        always_str = f'always {self.visit_expression(node.event_control)}'
        self.emit(always_str)
        self.emit('begin')
        self.indent_level += 1
        for stmt in node.statements:
            self.visit(stmt)
        self.indent_level -= 1
        self.emit('end')

    def visit_EventControl(self, node):
        """访问事件控制"""
        return f'@({self.visit_expression(node.event_expression)})'

    def visit_EventExpression(self, node):
        """访问事件表达式"""
        if node.edge_type == 'posedge':
            return f'posedge {self.visit_expression(node.expression)}'
        elif node.edge_type == 'negedge':
            return f'negedge {self.visit_expression(node.expression)}'
        else:
            return self.visit_expression(node.expression)

    def visit_BlockingAssignment(self, node):
        """访问阻塞赋值"""
        assign_str = f'{self.visit_expression(node.lvalue)} = {self.visit_expression(node.rvalue)}'
        self.emit(assign_str + ';')

    def visit_NonblockingAssignment(self, node):
        """访问非阻塞赋值"""
        assign_str = f'{self.visit_expression(node.lvalue)} <= {self.visit_expression(node.rvalue)}'
        self.emit(assign_str + ';')

    def visit_Assignment(self, node):
        """访问赋值语句（兼容性）"""
        assign_str = f'{self.visit_expression(node.lvalue)} = {self.visit_expression(node.rvalue)}'
        self.emit(assign_str + ';')

    def visit_IfStatement(self, node):
        """访问if语句"""
        if_str = f'if ({self.visit_expression(node.condition)})'
        self.emit(if_str)
        
        if len(node.then_statements) == 1:
            self.indent_level += 1
            self.visit(node.then_statements[0])
            self.indent_level -= 1
        else:
            self.emit('begin')
            self.indent_level += 1
            for stmt in node.then_statements:
                self.visit(stmt)
            self.indent_level -= 1
            self.emit('end')
        
        if node.else_statements:
            self.emit('else')
            if isinstance(node.else_statements, IfStatement):
                # elsif情况
                self.visit(node.else_statements)
            else:
                if len(node.else_statements) == 1:
                    self.indent_level += 1
                    self.visit(node.else_statements[0])
                    self.indent_level -= 1
                else:
                    self.emit('begin')
                    self.indent_level += 1
                    for stmt in node.else_statements:
                        self.visit(stmt)
                    self.indent_level -= 1
                    self.emit('end')

    def visit_CaseStatement(self, node):
        """访问case语句"""
        case_str = f'case ({self.visit_expression(node.expression)})'
        self.emit(case_str)
        self.indent_level += 1
        
        for case_item in node.case_items:
            if case_item.expression is None:
                self.emit('default:')
            else:
                self.emit(f'{self.visit_expression(case_item.expression)}:')
            
            if len(case_item.statements) == 1:
                self.indent_level += 1
                self.visit(case_item.statements[0])
                self.indent_level -= 1
            else:
                self.emit('begin')
                self.indent_level += 1
                for stmt in case_item.statements:
                    self.visit(stmt)
                self.indent_level -= 1
                self.emit('end')
        
        self.indent_level -= 1
        self.emit('endcase')

    def visit_expression(self, node):
        """访问表达式（返回字符串）"""
        if isinstance(node, BinaryExpression) or isinstance(node, BinaryOp):
            left = self.visit_expression(node.left)
            right = self.visit_expression(node.right)
            return f'({left} {node.operator} {right})'
        elif isinstance(node, UnaryExpression):
            operand = self.visit_expression(node.operand)
            return f'({node.operator}{operand})'
        elif isinstance(node, ConditionalExpression):
            cond = self.visit_expression(node.condition)
            true_expr = self.visit_expression(node.true_expr)
            false_expr = self.visit_expression(node.false_expr)
            return f'({cond} ? {true_expr} : {false_expr})'
        elif isinstance(node, IdentifierExpression) or isinstance(node, Identifier):
            return node.name
        elif isinstance(node, NumberExpression) or isinstance(node, Number):
            if isinstance(node.value, str):
                return node.value  # 已经是格式化的数字字符串
            else:
                return str(node.value)
        elif isinstance(node, NewNumberExpression):
            # 将新数值格式转换为Verilog格式
            return self.convert_new_number_format(node)
        elif isinstance(node, IndexExpression):
            return f'{self.visit_expression(node.array)}[{self.visit_expression(node.index)}]'
        elif isinstance(node, SliceExpression):
            return f'{self.visit_expression(node.array)}[{self.visit_expression(node.msb)}:{self.visit_expression(node.lsb)}]'
        elif isinstance(node, ConcatenationExpression):
            expr_list = [self.visit_expression(expr) for expr in node.expressions]
            return f'{{{", ".join(expr_list)}}}'
        elif isinstance(node, str):
            return node
        elif isinstance(node, int):
            return str(node)
        else:
            return str(node)

    def convert_new_number_format(self, node):
        """将新数值格式转换为Verilog格式"""
        value = node.value
        base = node.base
        width = node.width
        
        # 根据进制转换
        if base == 'd':
            # 十进制
            if width:
                return f"{width}'d{value}"
            else:
                return str(value)
        elif base == 'b':
            # 二进制
            if isinstance(value, int):
                bin_str = bin(value)[2:]  # 去掉'0b'前缀
            else:
                bin_str = str(value)
            if width:
                return f"{width}'b{bin_str}"
            else:
                return f"'b{bin_str}"
        elif base == 'h':
            # 十六进制
            if isinstance(value, int):
                hex_str = hex(value)[2:].upper()  # 去掉'0x'前缀并转大写
            else:
                hex_str = str(value).upper()
            if width:
                return f"{width}'h{hex_str}"
            else:
                return f"'h{hex_str}"
        elif base == 'o':
            # 八进制
            if isinstance(value, int):
                oct_str = oct(value)[2:]  # 去掉'0o'前缀
            else:
                oct_str = str(value)
            if width:
                return f"{width}'o{oct_str}"
            else:
                return f"'o{oct_str}"
        else:
            # 默认十进制
            if width:
                return f"{width}'d{value}"
            else:
                return str(value)

if __name__ == "__main__":
    # 测试代码生成器
    from .parser import GraceHDLParser
    
    parser = GraceHDLParser()
    parser.build()
    
    test_code = """
module counter
    input:
        wire clk, reset
    output:
        reg[7:0] count
    
    run posedge clk:
        if reset
            count = (0, d, 8)
        else
            count = count + (1, d, 8)
"""
    
    try:
        ast = parser.parser.parse(test_code, lexer=parser.lexer.lexer)
        
        generator = VerilogGenerator()
        verilog_code = generator.generate(ast)
        print("生成的Verilog代码:")
        print(verilog_code)
    except Exception as e:
        print(f"测试失败: {e}")