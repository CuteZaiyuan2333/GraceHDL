"""
Verilog代码生成器 - 新语法版本
将GraceHDL的AST转换为标准Verilog HDL代码
支持新的数值格式和run/always语句
"""

try:
    from .ast_nodes import *
except ImportError:
    from ast_nodes import *

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
    
    def visit_str(self, node):
        """处理字符串值"""
        return node

    def visit_CommentNode(self, node):
        """访问注释节点"""
        # 直接输出注释，保持原格式
        self.emit(node.content)

    def visit_SourceText(self, node):
        """访问源代码根节点"""
        # 首先处理所有非模块项（如枚举声明）
        for item in node.items:
            if item is not None and not isinstance(item, ModuleDeclaration):
                self.visit(item)
                self.emit('')  # 项目间空行
        
        # 然后处理模块
        for module in node.modules:
            self.visit(module)
            self.emit('')  # 模块间空行

    def visit_ModuleDeclaration(self, node):
        """访问模块声明"""
        # 收集所有端口信息
        input_ports = []
        output_ports = []
        reg_declarations = []
        
        # 从sections中收集端口信息
        for section in node.sections:
            if isinstance(section, InputSection):
                for port in section.ports:
                    if port is not None and isinstance(port, PortDeclaration):
                        input_ports.extend([(name, port.net_type, port.range_spec) for name in port.names])
            elif isinstance(section, OutputSection):
                for port in section.ports:
                    if port is not None and isinstance(port, PortDeclaration):
                        # 检查是否在always块中被赋值，如果是则需要声明为reg
                        for name in port.names:
                            is_reg = self.is_signal_assigned_in_always(name, node.sections)
                            port_type = 'reg' if is_reg else 'wire'
                            output_ports.append((name, port_type, port.range_spec))
        
        # 生成ANSI风格的模块头
        module_header = f'module {node.name}'
        
        # 参数列表
        if node.parameters:
            param_list = []
            for param in node.parameters:
                param_str = f'parameter {param.name} = {self.visit_expression(param.value)}'
                param_list.append(param_str)
            module_header += f' #({", ".join(param_list)})'
        
        # ANSI风格端口列表
        port_list = []
        
        # 添加输入端口
        for name, net_type, range_spec in input_ports:
            port_str = f'input {net_type}'
            if range_spec:
                port_str += f'[{self.visit_expression(range_spec.msb)}:{self.visit_expression(range_spec.lsb)}]'
            port_str += f' {name}'
            port_list.append(port_str)
        
        # 添加输出端口
        for name, port_type, range_spec in output_ports:
            port_str = f'output {port_type}'
            if range_spec:
                port_str += f'[{self.visit_expression(range_spec.msb)}:{self.visit_expression(range_spec.lsb)}]'
            port_str += f' {name}'
            port_list.append(port_str)
        
        if port_list:
            if len(port_list) == 1:
                module_header += f'({port_list[0]})'
            else:
                module_header += '(\n'
                for i, port in enumerate(port_list):
                    if i == len(port_list) - 1:
                        module_header += f'    {port}\n'
                    else:
                        module_header += f'    {port},\n'
                module_header += ')'
        
        self.emit(module_header + ';')
        self.emit('')
        
        # 模块内容 - 跳过输入输出声明，只处理其他sections
        self.indent_level += 1
        for section in node.sections:
            if not isinstance(section, (InputSection, OutputSection)):
                self.visit(section)
                self.emit('')  # 段落间空行
        self.indent_level -= 1
        
        self.emit('endmodule')

    def is_signal_assigned_in_always(self, signal_name, sections):
        """检查信号是否在always块中被赋值"""
        for section in sections:
            if isinstance(section, AlwaysSection):
                # 检查always块中的赋值语句
                if self.check_assignments_in_statements(signal_name, section.statements):
                    return True
        return False
    
    def check_assignments_in_statements(self, signal_name, statements):
        """递归检查语句列表中是否有对指定信号的赋值"""
        if not statements:
            return False
        
        for stmt in statements:
            if hasattr(stmt, 'target'):
                # 处理字符串类型的target
                if isinstance(stmt.target, str):
                    if stmt.target == signal_name:
                        return True
                # 处理对象类型的target
                elif hasattr(stmt.target, 'name'):
                    if stmt.target.name == signal_name:
                        return True
            # 检查case语句
            elif hasattr(stmt, 'case_items'):
                for case_item in stmt.case_items:
                    if hasattr(case_item, 'statements'):
                        if self.check_assignments_in_statements(signal_name, case_item.statements):
                            return True
            # 检查if语句
            elif hasattr(stmt, 'then_statements'):
                if self.check_assignments_in_statements(signal_name, stmt.then_statements):
                    return True
                if hasattr(stmt, 'else_statements') and stmt.else_statements:
                    if self.check_assignments_in_statements(signal_name, stmt.else_statements):
                        return True
        return False

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
            if port is not None:  # 跳过None值（来自注释或换行）
                self.visit(port)

    def visit_OutputSection(self, node):
        """访问输出端口段"""
        for port in node.ports:
            if port is not None:  # 跳过None值（来自注释或换行）
                self.visit(port)

    def visit_RegisterSection(self, node):
        """访问寄存器段"""
        for register in node.registers:
            if register is not None:  # 跳过None值（来自注释或换行）
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
            if stmt is not None:
                self.visit(stmt)
        self.indent_level -= 1
        self.emit('end')

    def visit_AlwaysSection(self, node):
        """访问always语句段（组合逻辑）"""
        # 使用标准的always @(*) 语法而不是always_comb
        self.emit('always @(*)')
        self.emit('begin')
        self.indent_level += 1
        
        # 处理语句，检测并修复case语句的贪婪匹配问题
        statements_to_process = []
        i = 0
        while i < len(node.statements):
            stmt = node.statements[i]
            if hasattr(stmt, '__class__') and stmt.__class__.__name__ == 'CaseStatement':
                # 检测case语句的最后一个case_item是否包含了过多的语句
                fixed_case, extracted_statements = self.fix_case_statement_greedy_matching(stmt)
                statements_to_process.append(fixed_case)
                statements_to_process.extend(extracted_statements)
            else:
                statements_to_process.append(stmt)
            i += 1
        
        for stmt in statements_to_process:
            if stmt is not None:
                self.visit(stmt)
        self.indent_level -= 1
        self.emit('end')

    def visit_AssignSection(self, node):
        """访问assign语句段（连续赋值）"""
        # assign块中的每个赋值语句都转换为Verilog的assign语句
        for assignment in node.assignments:
            if assignment is not None:
                if hasattr(assignment, 'target') and hasattr(assignment, 'expression'):
                    # 这是一个赋值语句
                    if isinstance(assignment.target, str):
                        target = assignment.target
                    else:
                        target = self.visit_expression(assignment.target)
                    
                    expr = self.visit_expression(assignment.expression)
                    self.emit(f'assign {target} = {expr};')
                else:
                    # 这可能是注释或其他节点
                    self.visit(assignment)
    
    def fix_case_statement_greedy_matching(self, case_stmt):
        """修复case语句的贪婪匹配问题"""
        if not case_stmt.case_items:
            return case_stmt, []
        
        # 获取最后一个case_item
        last_case_item = case_stmt.case_items[-1]
        
        # 如果最后一个case_item是default且包含多个语句，检查是否有误归属的语句
        if (last_case_item.expression is None and  # default case
            len(last_case_item.statements) > 1):
            
            # 简单的启发式：如果default case包含超过2个语句，
            # 假设最后的语句可能是误归属的
            if len(last_case_item.statements) > 2:
                # 保留前面的语句作为default case的内容
                correct_statements = last_case_item.statements[:-2]
                extracted_statements = last_case_item.statements[-2:]
                
                # 创建新的case_item
                from src.ast_nodes import CaseItem
                new_last_case_item = CaseItem(None, correct_statements)
                
                # 创建新的case语句
                new_case_items = case_stmt.case_items[:-1] + [new_last_case_item]
                new_case_stmt = case_stmt.__class__(case_stmt.expression, new_case_items)
                
                return new_case_stmt, extracted_statements
        
        return case_stmt, []

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

    def visit_ArrayRegisterDeclaration(self, node):
        """访问数组寄存器声明"""
        range_str = ""
        if node.range_spec:
            range_str = self.visit(node.range_spec) + " "
        
        array_range_str = self.visit(node.array_range)
        self.emit(f"reg {range_str}{node.identifier} {array_range_str};")

    def visit_ParameterDeclaration(self, node):
        """访问参数声明"""
        param_str = f'parameter {node.name} = {self.visit_expression(node.value)}'
        self.emit(param_str + ';')

    def visit_AssignmentStatement(self, node):
        """访问赋值语句"""
        # 在run块中使用非阻塞赋值，在always块中使用阻塞赋值
        if isinstance(node.target, str):
            # 普通变量赋值
            assign_str = f'{node.target} = {self.visit_expression(node.expression)}'
        else:
            # 数组索引或切片赋值
            target = self.visit_expression(node.target)
            assign_str = f'{target} = {self.visit_expression(node.expression)}'
        self.emit(assign_str + ';')

    def visit_ToAssignmentStatement(self, node):
        """访问to赋值语句（时序逻辑赋值）"""
        # to语句总是使用非阻塞赋值（<=）
        if isinstance(node.target, str):
            # 普通变量赋值
            assign_str = f'{node.target} <= {self.visit_expression(node.expression)}'
        else:
            # 数组索引或切片赋值
            target = self.visit_expression(node.target)
            assign_str = f'{target} <= {self.visit_expression(node.expression)}'
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
        
        # 处理elif语句
        if hasattr(node, 'elif_statements') and node.elif_statements:
            for elif_stmt in node.elif_statements:
                self.emit(f'else if ({self.visit_expression(elif_stmt.condition)})')
                if len(elif_stmt.statements) == 1:
                    self.indent_level += 1
                    self.visit(elif_stmt.statements[0])
                    self.indent_level -= 1
                else:
                    self.emit('begin')
                    self.indent_level += 1
                    for stmt in elif_stmt.statements:
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

    def visit_ElifStatement(self, node):
        """访问elif语句"""
        # elif语句在visit_IfStatement中处理，这里只是为了兼容性
        pass

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

    def visit_ForStatement(self, node):
        """访问for语句 - 展开循环生成多个硬件结构"""
        # For语句在编译时展开，生成多个硬件结构
        loop_var = node.loop_var
        range_expr = node.range_expr
        
        # 计算range表达式的值
        start = self.evaluate_expression(range_expr.start)
        end = self.evaluate_expression(range_expr.end)
        step = 1 if range_expr.step is None else self.evaluate_expression(range_expr.step)
        
        # 为每个循环值生成代码（编译时展开）
        current = start
        while (step > 0 and current < end) or (step < 0 and current > end):
            # 创建一个临时的参数替换环境
            old_params = getattr(self, 'loop_params', {})
            self.loop_params = old_params.copy()
            self.loop_params[loop_var] = current
            
            # 生成当前循环迭代的代码
            for stmt in node.statements:
                self.visit(stmt)
            
            # 恢复参数环境
            self.loop_params = old_params
            current += step

    def visit_RangeExpression(self, node):
        """访问range表达式"""
        # range表达式在for语句中处理，这里只是为了兼容性
        return node

    def evaluate_expression(self, expr):
        """计算表达式的值（用于编译时常量）"""
        if isinstance(expr, NumberExpression) or isinstance(expr, Number):
            return int(expr.value) if isinstance(expr.value, (int, str)) and str(expr.value).isdigit() else expr.value
        elif isinstance(expr, IdentifierExpression) or isinstance(expr, Identifier):
            # 检查是否是参数或循环变量
            if hasattr(self, 'parameters') and expr.name in self.parameters:
                return self.parameters[expr.name]
            elif hasattr(self, 'loop_params') and expr.name in self.loop_params:
                return self.loop_params[expr.name]
            else:
                return expr.name  # 返回标识符名称
        elif isinstance(expr, BinaryExpression):
            left = self.evaluate_expression(expr.left)
            right = self.evaluate_expression(expr.right)
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                if expr.operator == '+':
                    return left + right
                elif expr.operator == '-':
                    return left - right
                elif expr.operator == '*':
                    return left * right
                elif expr.operator == '/':
                    return left // right  # 整数除法
                else:
                    return f"({left} {expr.operator} {right})"
            else:
                return f"({left} {expr.operator} {right})"
        elif isinstance(expr, int):
            return expr
        else:
            return str(expr)

    def visit_ModuleInstantiation(self, node):
        """访问模块实例化"""
        # 生成模块实例化语句
        if node.port_connections:
            # 有端口连接
            port_list = []
            for conn in node.port_connections:
                if conn.signal_name:
                    port_list.append(f'.{conn.port_name}({conn.signal_name})')
                else:
                    port_list.append(f'.{conn.port_name}()')
            
            port_str = ', '.join(port_list)
            self.emit(f'{node.module_name} {node.instance_name} ({port_str});')
        else:
            # 无端口连接
            self.emit(f'{node.module_name} {node.instance_name} ();')

    def visit_BinaryExpression(self, node):
        """访问二元表达式"""
        left = self.visit(node.left)
        right = self.visit(node.right)
        return f"({left} {node.operator} {right})"

    def visit_UnaryExpression(self, node):
        """访问一元表达式"""
        operand = self.visit(node.operand)
        return f"({node.operator}{operand})"

    def visit_IndexExpression(self, node):
        """访问数组索引表达式"""
        array = node.array
        index = self.visit(node.index)
        return f"{array}[{index}]"

    def visit_SliceExpression(self, node):
        """访问数组切片表达式"""
        array = node.array
        msb = self.visit(node.msb)
        lsb = self.visit(node.lsb)
        return f"{array}[{msb}:{lsb}]"

    def visit_RangeSpec(self, node):
        """访问范围规格"""
        msb = self.visit(node.msb)
        lsb = self.visit(node.lsb)
        return f"[{msb}:{lsb}]"
    
    def visit_int(self, node):
        """访问整数"""
        return str(node)

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
            # 检查是否是循环变量，如果是则替换为当前值
            if hasattr(self, 'loop_params') and node.name in self.loop_params:
                return str(self.loop_params[node.name])
            else:
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
            array_name = node.array
            # 检查数组名是否是循环变量，如果是则替换
            if hasattr(self, 'loop_params') and array_name in self.loop_params:
                array_name = str(self.loop_params[array_name])
            index = self.visit_expression(node.index)
            return f'{array_name}[{index}]'
        elif isinstance(node, SliceExpression):
            return f'{self.visit_expression(node.array)}[{self.visit_expression(node.msb)}:{self.visit_expression(node.lsb)}]'
        elif isinstance(node, ConcatenationExpression):
            expr_list = [self.visit_expression(expr) for expr in node.expressions]
            return f'{{{", ".join(expr_list)}}}'
        elif isinstance(node, EnumReference):
            return self.visit_EnumReference(node)
        elif isinstance(node, FunctionCall):
            return self.visit_FunctionCall(node)
        elif isinstance(node, ReduceOperation):
            return self.visit_ReduceOperation(node)
        elif isinstance(node, str):
            return node
        elif isinstance(node, int):
            return str(node)
        else:
            return str(node)

    def visit_NewNumberExpression(self, node):
        """访问新数值格式表达式"""
        # 转换为Verilog格式
        if node.base == 'd':
            return f"{node.width}'{node.value}"
        elif node.base == 'b':
            return f"{node.width}'b{bin(node.value)[2:].zfill(node.width)}"
        elif node.base == 'h':
            return f"{node.width}'h{hex(node.value)[2:].upper()}"
        elif node.base == 'o':
            return f"{node.width}'o{oct(node.value)[2:]}"
        else:
            return str(node.value)

    # 新语法特性的访问方法

    def visit_EnumDeclaration(self, node):
        """访问枚举类型声明"""
        # 在Verilog中，枚举类型转换为参数定义
        self.emit(f'// Enum {node.name}')
        for i, item in enumerate(node.items):
            if item is not None and hasattr(item, 'name') and item.name:
                if item.value is not None:
                    self.emit(f'localparam {node.name}_{item.name} = {self.visit_expression(item.value)};')
                else:
                    # 如果没有指定值，使用递增的值（从1开始）
                    self.emit(f'localparam {node.name}_{item.name} = {i + 1};')

    def visit_EnumItem(self, node):
        """访问枚举项"""
        # 这个方法通常不会直接调用，因为枚举项在EnumDeclaration中处理
        pass

    def visit_EnumReference(self, node):
        """访问枚举引用"""
        # 转换为参数引用
        return f'{node.enum_name}_{node.item_name}'

    def visit_FunctionDeclaration(self, node):
        """访问函数声明"""
        # 在Verilog中，函数转换为function定义
        param_list = ', '.join([param.name for param in node.parameters])
        self.emit(f'function automatic [{self.get_function_width(node)}:0] {node.name};')
        if param_list:
            self.emit(f'    input [{self.get_function_width(node)}:0] {param_list};')
        self.indent_level += 1
        self.emit('begin')
        self.indent_level += 1
        
        for stmt in node.statements:
            if stmt is not None:
                self.visit(stmt)
        
        self.indent_level -= 1
        self.emit('end')
        self.indent_level -= 1
        self.emit('endfunction')

    def get_function_width(self, node):
        """获取函数的位宽（简化实现）"""
        # 这里简化为32位，实际应该根据函数内容推断
        return "31"

    def visit_FunctionParameter(self, node):
        """访问函数参数"""
        # 在函数声明中处理
        pass

    def visit_ReturnStatement(self, node):
        """访问return语句"""
        # 在Verilog函数中，return语句转换为函数名赋值
        func_name = "result"  # 简化处理
        self.emit(f'{func_name} = {self.visit_expression(node.expression)};')

    def visit_FunctionCall(self, node):
        """访问函数调用"""
        if node.arguments:
            args = ', '.join([self.visit_expression(arg) for arg in node.arguments])
            return f'{node.name}({args})'
        else:
            return f'{node.name}()'

    def visit_InterfaceDeclaration(self, node):
        """访问接口声明"""
        # 在Verilog中，接口转换为模块定义
        self.emit(f'// Interface {node.name}')
        # 接口在Verilog中通常转换为端口组合或模块
        # 这里简化处理，实际需要更复杂的转换逻辑

    def visit_PortDeclarationInterface(self, node):
        """访问接口端口声明"""
        # 接口端口在模块中的处理
        pass

    def visit_GenerateSection(self, node):
        """访问generate语句段"""
        self.emit('generate')
        self.indent_level += 1
        for stmt in node.statements:
            if stmt is not None:
                self.visit(stmt)
        self.indent_level -= 1
        self.emit('endgenerate')

    def visit_ForGenerateStatement(self, node):
        """访问for生成语句"""
        # 转换为Verilog的genvar和for循环
        self.emit(f'genvar {node.variable};')
        start_expr = self.visit_expression(node.start)
        end_expr = self.visit_expression(node.end)
        
        if node.step and self.visit_expression(node.step) != "1":
            # 如果有步长且不为1，需要特殊处理
            self.emit(f'for ({node.variable} = {start_expr}; {node.variable} < {end_expr}; {node.variable} = {node.variable} + {self.visit_expression(node.step)}) begin')
        else:
            self.emit(f'for ({node.variable} = {start_expr}; {node.variable} < {end_expr}; {node.variable} = {node.variable} + 1) begin')
        
        self.indent_level += 1
        for stmt in node.statements:
            if stmt is not None:
                self.visit(stmt)
        self.indent_level -= 1
        self.emit('end')

    def visit_AssertStatement(self, node):
        """访问断言语句"""
        # 转换为Verilog的assert语句
        if node.message:
            self.emit(f'assert ({self.visit_expression(node.condition)}) else $error({node.message});')
        else:
            self.emit(f'assert ({self.visit_expression(node.condition)});')

    def visit_CoverStatement(self, node):
        """访问覆盖率语句"""
        # 转换为Verilog的cover语句
        if node.message:
            self.emit(f'cover ({self.visit_expression(node.condition)}) $display({node.message});')
        else:
            self.emit(f'cover ({self.visit_expression(node.condition)});')

    def visit_ClockedRegisterDeclaration(self, node):
        """访问带时钟域的寄存器声明"""
        # 在Verilog中，时钟域信息通过always块体现
        # 这里只生成寄存器声明，时钟域在always块中处理
        if node.range_spec:
            range_str = f'[{self.visit_expression(node.range_spec.msb)}:{self.visit_expression(node.range_spec.lsb)}]'
            self.emit(f'reg {range_str} {", ".join(node.names)};')
        else:
            self.emit(f'reg {", ".join(node.names)};')

    def visit_ReduceOperation(self, node):
        """访问归约运算"""
        # 转换为Verilog的归约运算符
        if node.operator == 'and':
            return f'&({self.visit_expression(node.operand)})'
        elif node.operator == 'or':
            return f'|({self.visit_expression(node.operand)})'
        elif node.operator == 'xor':
            return f'^({self.visit_expression(node.operand)})'
        else:
            return f'{node.operator}({self.visit_expression(node.operand)})'

    def visit_TestbenchDeclaration(self, node):
        """访问测试台声明"""
        # 生成测试台模块
        self.emit(f'module tb_{node.module_name};')
        self.indent_level += 1
        
        # 生成测试台内容
        for section in node.body:
            if section is not None:
                self.visit(section)
        
        self.indent_level -= 1
        self.emit('endmodule')

    def visit_ClockDeclaration(self, node):
        """访问时钟声明"""
        # 生成时钟信号和时钟生成逻辑
        self.emit(f'reg {node.clock_name};')
        self.emit(f'initial begin')
        self.indent_level += 1
        self.emit(f'{node.clock_name} = 0;')
        period_value = self.visit_expression(node.period)
        # 计算半周期，如果是数字则直接计算，否则生成表达式
        try:
            half_period = int(period_value) // 2
            self.emit(f'forever #{half_period} {node.clock_name} = ~{node.clock_name};')
        except (ValueError, TypeError):
            self.emit(f'forever #({period_value}/2) {node.clock_name} = ~{node.clock_name};')
        self.indent_level -= 1
        self.emit('end')

    def visit_SignalDeclaration(self, node):
        """访问信号声明"""
        # 生成测试信号
        if node.signal_type == 'reg':
            if node.range_spec:
                width_str = f'[{self.visit_expression(node.range_spec.msb)}:{self.visit_expression(node.range_spec.lsb)}]'
                self.emit(f'reg {width_str} {node.signal_name};')
            else:
                self.emit(f'reg {node.signal_name};')
        elif node.signal_type == 'wire':
            if node.range_spec:
                width_str = f'[{self.visit_expression(node.range_spec.msb)}:{self.visit_expression(node.range_spec.lsb)}]'
                self.emit(f'wire {width_str} {node.signal_name};')
            else:
                self.emit(f'wire {node.signal_name};')

    def visit_DutInstantiation(self, node):
        """访问被测模块实例化"""
        # 生成模块实例化
        if node.parameters:
            param_str = '#(' + ', '.join([f'.{p.name}({self.visit_expression(p.value)})' for p in node.parameters]) + ')'
            self.emit(f'{node.module_name} {param_str} dut (')
        else:
            self.emit(f'{node.module_name} dut (')
        
        self.indent_level += 1
        port_connections = []
        for conn in node.port_connections:
            port_connections.append(f'.{conn.port_name}({conn.signal_name})')
        
        for i, conn in enumerate(port_connections):
            if i == len(port_connections) - 1:
                self.emit(conn)
            else:
                self.emit(conn + ',')
        
        self.indent_level -= 1
        self.emit(');')

    def visit_TestSequence(self, node):
        """访问测试序列"""
        # 生成initial块
        self.emit('initial begin')
        self.indent_level += 1
        
        for stmt in node.statements:
            if stmt is not None:
                self.visit(stmt)
        
        self.emit('$finish;')
        self.indent_level -= 1
        self.emit('end')

    def visit_WaitStatement(self, node):
        """访问等待语句"""
        # 转换为Verilog的延时语句
        delay_value = self.visit_expression(node.duration)
        self.emit(f'#{delay_value};')

    def visit_DumpWavesStatement(self, node):
        """访问波形输出语句"""
        # 生成VCD文件输出
        self.emit('$dumpfile("waves.vcd");')
        self.emit('$dumpvars(0, dut);')

    def visit_ReportCoverageStatement(self, node):
        """访问覆盖率报告语句"""
        # 生成覆盖率报告
        self.emit('$display("Coverage report generated");')

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