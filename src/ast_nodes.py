"""
GraceHDL抽象语法树节点定义 - 新语法版本
定义所有AST节点类，用于表示解析后的新GraceHDL语法结构
"""

class ASTNode:
    """AST节点基类"""
    pass

class CommentNode(ASTNode):
    """注释节点"""
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return f"CommentNode({self.content})"

class SourceText(ASTNode):
    """源代码根节点"""
    def __init__(self, modules, items=None):
        self.modules = modules
        self.items = items or []  # 所有源代码项（包括枚举、函数等）

    def __repr__(self):
        return f"SourceText({self.modules})"

class ModuleDeclaration(ASTNode):
    """模块声明"""
    def __init__(self, name, parameters, ports, sections):
        self.name = name
        self.parameters = parameters or []
        self.ports = ports or []
        self.sections = sections or []

    def __repr__(self):
        return f"ModuleDeclaration({self.name}, {self.parameters}, {self.ports}, {self.sections})"

# 新的语法节点

class InputSection(ASTNode):
    """输入端口段"""
    def __init__(self, ports):
        self.ports = ports or []

    def __repr__(self):
        return f"InputSection({self.ports})"

class OutputSection(ASTNode):
    """输出端口段"""
    def __init__(self, ports):
        self.ports = ports or []

    def __repr__(self):
        return f"OutputSection({self.ports})"

class RegisterSection(ASTNode):
    """寄存器段"""
    def __init__(self, registers):
        self.registers = registers or []

    def __repr__(self):
        return f"RegisterSection({self.registers})"

class ParameterSection(ASTNode):
    """参数段"""
    def __init__(self, parameters):
        self.parameters = parameters or []

    def __repr__(self):
        return f"ParameterSection({self.parameters})"

class RunSection(ASTNode):
    """run语句段（时序逻辑）"""
    def __init__(self, clock_edge, statements):
        self.clock_edge = clock_edge
        self.statements = statements or []

    def __repr__(self):
        return f"RunSection({self.clock_edge}, {self.statements})"

class AlwaysSection(ASTNode):
    """always语句段（组合逻辑）"""
    def __init__(self, statements):
        self.statements = statements or []

    def __repr__(self):
        return f"AlwaysSection({self.statements})"

class AssignSection(ASTNode):
    """assign语句段（连续赋值）"""
    def __init__(self, assignments):
        self.assignments = assignments or []

    def __repr__(self):
        return f"AssignSection({self.assignments})"

class ClockEdge(ASTNode):
    """时钟边沿"""
    def __init__(self, signal, edge_type):
        self.signal = signal
        self.edge_type = edge_type  # 'posedge' or 'negedge'

    def __repr__(self):
        return f"ClockEdge({self.signal}, {self.edge_type})"

class PortDeclaration(ASTNode):
    """端口声明"""
    def __init__(self, direction, net_type, range_spec, names):
        self.direction = direction
        self.net_type = net_type
        self.range_spec = range_spec
        self.names = names

    def __repr__(self):
        return f"PortDeclaration({self.direction}, {self.net_type}, {self.range_spec}, {self.names})"

class RegisterDeclaration(ASTNode):
    """寄存器声明"""
    def __init__(self, range_spec, names):
        self.range_spec = range_spec
        self.names = names

    def __repr__(self):
        return f"RegisterDeclaration({self.range_spec}, {self.names})"

class ArrayRegisterDeclaration(ASTNode):
    def __init__(self, range_spec, identifier, array_range):
        self.range_spec = range_spec  # 位宽范围，如 (7:0)
        self.identifier = identifier  # 数组名
        self.array_range = array_range  # 数组范围，如 [255:0]

    def __repr__(self):
        return f"ArrayRegisterDeclaration({self.range_spec}, {self.identifier}, {self.array_range})"

class ParameterDeclaration(ASTNode):
    """参数声明"""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"ParameterDeclaration({self.name}, {self.value})"

class RangeSpec(ASTNode):
    """位宽范围规格"""
    def __init__(self, msb, lsb):
        self.msb = msb
        self.lsb = lsb

    def __repr__(self):
        return f"RangeSpec({self.msb}, {self.lsb})"

# 语句节点

class AssignmentStatement(ASTNode):
    """赋值语句"""
    def __init__(self, target, expression):
        self.target = target
        self.expression = expression

    def __repr__(self):
        return f"AssignmentStatement({self.target}, {self.expression})"

class ToAssignmentStatement(ASTNode):
    """to赋值语句（时序逻辑赋值）"""
    def __init__(self, expression, target):
        self.expression = expression  # 源值
        self.target = target         # 目标变量

    def __repr__(self):
        return f"ToAssignmentStatement({self.expression}, {self.target})"

class IfStatement(ASTNode):
    """if语句"""
    def __init__(self, condition, then_statements, else_statements=None, elif_statements=None):
        self.condition = condition
        self.then_statements = then_statements or []
        self.else_statements = else_statements or []
        self.elif_statements = elif_statements or []

    def __repr__(self):
        return f"IfStatement({self.condition}, {self.then_statements}, {self.else_statements}, {self.elif_statements})"

class ElifStatement(ASTNode):
    """elif语句"""
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements or []

    def __repr__(self):
        return f"ElifStatement({self.condition}, {self.statements})"

class CaseStatement(ASTNode):
    """case语句"""
    def __init__(self, expression, case_items):
        self.expression = expression
        self.case_items = case_items or []

    def __repr__(self):
        return f"CaseStatement({self.expression}, {self.case_items})"

class CaseItem(ASTNode):
    """case项"""
    def __init__(self, expression, statements):
        self.expression = expression  # None for default case
        self.statements = statements or []

    def __repr__(self):
        return f"CaseItem({self.expression}, {self.statements})"

# 枚举类型节点

class EnumDeclaration(ASTNode):
    """枚举类型声明"""
    def __init__(self, name, items):
        self.name = name
        # 过滤掉None项和空名称项
        self.items = [item for item in (items or []) if item is not None and hasattr(item, 'name') and item.name and item.name.strip()]

    def __repr__(self):
        return f"EnumDeclaration({self.name}, {self.items})"

class EnumItem(ASTNode):
    """枚举项"""
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"EnumItem({self.name}, {self.value})"

class EnumReference(ASTNode):
    """枚举引用（如 State.IDLE）"""
    def __init__(self, enum_name, item_name):
        self.enum_name = enum_name
        self.item_name = item_name

    def __repr__(self):
        return f"EnumReference({self.enum_name}, {self.item_name})"

# 函数定义节点

class FunctionDeclaration(ASTNode):
    """函数声明"""
    def __init__(self, name, parameters, statements):
        self.name = name
        self.parameters = parameters or []
        self.statements = statements or []

    def __repr__(self):
        return f"FunctionDeclaration({self.name}, {self.parameters}, {self.statements})"

class FunctionParameter(ASTNode):
    """函数参数"""
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"FunctionParameter({self.name})"

class ReturnStatement(ASTNode):
    """return语句"""
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"ReturnStatement({self.expression})"

class FunctionCall(ASTNode):
    """函数调用"""
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments or []

    def __repr__(self):
        return f"FunctionCall({self.name}, {self.arguments})"

# 接口定义节点

class InterfaceDeclaration(ASTNode):
    """接口声明"""
    def __init__(self, name, parameters, ports):
        self.name = name
        self.parameters = parameters or []
        self.ports = ports or []

    def __repr__(self):
        return f"InterfaceDeclaration({self.name}, {self.parameters}, {self.ports})"

class PortDeclarationInterface(ASTNode):
    """接口端口声明"""
    def __init__(self, interface_name, instance_name, parameters=None):
        self.interface_name = interface_name
        self.instance_name = instance_name
        self.parameters = parameters or []

    def __repr__(self):
        return f"PortDeclarationInterface({self.interface_name}, {self.instance_name}, {self.parameters})"

# 生成语句节点

class GenerateSection(ASTNode):
    """generate语句段"""
    def __init__(self, statements):
        self.statements = statements or []

    def __repr__(self):
        return f"GenerateSection({self.statements})"

class ForGenerateStatement(ASTNode):
    """for生成语句"""
    def __init__(self, variable, start, end, step, statements):
        self.variable = variable
        self.start = start
        self.end = end
        self.step = step
        self.statements = statements or []

    def __repr__(self):
        return f"ForGenerateStatement({self.variable}, {self.start}, {self.end}, {self.step}, {self.statements})"

# 断言节点

class AssertStatement(ASTNode):
    """断言语句"""
    def __init__(self, condition, message=None):
        self.condition = condition
        self.message = message

    def __repr__(self):
        return f"AssertStatement({self.condition}, {self.message})"

class CoverStatement(ASTNode):
    """覆盖率语句"""
    def __init__(self, condition, message=None):
        self.condition = condition
        self.message = message

    def __repr__(self):
        return f"CoverStatement({self.condition}, {self.message})"

# 多时钟域节点

class ClockedRegisterDeclaration(ASTNode):
    """带时钟域的寄存器声明"""
    def __init__(self, range_spec, names, clock_signal):
        self.range_spec = range_spec
        self.names = names
        self.clock_signal = clock_signal

    def __repr__(self):
        return f"ClockedRegisterDeclaration({self.range_spec}, {self.names}, {self.clock_signal})"

# 归约运算符节点

class ReduceOperation(ASTNode):
    """归约运算"""
    def __init__(self, operator, operand):
        self.operator = operator  # 'and', 'or', 'xor'
        self.operand = operand

    def __repr__(self):
        return f"ReduceOperation({self.operator}, {self.operand})"

class ForStatement(ASTNode):
    """for循环生成语句"""
    def __init__(self, loop_var, range_expr, statements):
        self.loop_var = loop_var  # 循环变量名
        self.range_expr = range_expr  # range表达式
        self.statements = statements or []  # 循环体语句

    def __repr__(self):
        return f"ForStatement({self.loop_var}, {self.range_expr}, {self.statements})"

class ModuleInstantiation(ASTNode):
    """模块实例化"""
    def __init__(self, module_name, instance_name, port_connections):
        self.module_name = module_name
        self.instance_name = instance_name
        self.port_connections = port_connections or []

    def __repr__(self):
        return f"ModuleInstantiation({self.module_name}, {self.instance_name}, {self.port_connections})"

class PortConnection(ASTNode):
    """端口连接"""
    def __init__(self, port_name, signal_name):
        self.port_name = port_name
        self.signal_name = signal_name

    def __repr__(self):
        return f"PortConnection({self.port_name}, {self.signal_name})"

# 表达式节点

class Expression(ASTNode):
    """表达式基类"""
    pass

class IdentifierExpression(Expression):
    """标识符表达式"""
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"IdentifierExpression({self.name})"

class NumberExpression(Expression):
    """数字表达式"""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberExpression({self.value})"

class NewNumberExpression(Expression):
    """新数值格式表达式 (value, base, width)"""
    def __init__(self, value, base, width):
        self.value = value
        self.base = base
        self.width = width

    def __repr__(self):
        return f"NewNumberExpression({self.value}, {self.base}, {self.width})"

class BinaryExpression(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class UnaryExpression(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"BinaryExpression({self.operator}, {self.left}, {self.right})"

class UnaryExpression(Expression):
    """一元表达式"""
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"UnaryExpression({self.operator}, {self.operand})"

class ConditionalExpression(Expression):
    """条件表达式 (三元运算符)"""
    def __init__(self, condition, true_expr, false_expr):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr

    def __repr__(self):
        return f"ConditionalExpression({self.condition}, {self.true_expr}, {self.false_expr})"

class IndexExpression(Expression):
    """索引表达式"""
    def __init__(self, array, index):
        self.array = array
        self.index = index

    def __repr__(self):
        return f"IndexExpression({self.array}, {self.index})"

class SliceExpression(Expression):
    """切片表达式"""
    def __init__(self, array, msb, lsb):
        self.array = array
        self.msb = msb
        self.lsb = lsb

    def __repr__(self):
        return f"SliceExpression({self.array}, {self.msb}, {self.lsb})"

class ConcatenationExpression(Expression):
    """拼接表达式"""
    def __init__(self, expressions):
        self.expressions = expressions

    def __repr__(self):
        return f"ConcatenationExpression({self.expressions})"

class RangeExpression(Expression):
    """range表达式"""
    def __init__(self, start, end, step=None):
        self.start = start  # 起始值
        self.end = end      # 结束值
        self.step = step    # 步长（可选）

    def __repr__(self):
        if self.step:
            return f"RangeExpression({self.start}, {self.end}, {self.step})"
        else:
            return f"RangeExpression({self.start}, {self.end})"

# 兼容性节点（保持与旧版本的兼容）

class Range(RangeSpec):
    """位宽范围（兼容性别名）"""
    pass

class Assignment(AssignmentStatement):
    """赋值语句（兼容性别名）"""
    def __init__(self, lvalue, rvalue):
        super().__init__(lvalue, rvalue)

class Identifier(IdentifierExpression):
    """标识符（兼容性别名）"""
    pass

class Number(NumberExpression):
    """数字（兼容性别名）"""
    pass

class BinaryOp(BinaryExpression):
    """二元操作（兼容性别名）"""
    pass

class ContinuousAssign(ASTNode):
    """连续赋值（兼容性）"""
    def __init__(self, assignments):
        self.assignments = assignments

    def __repr__(self):
        return f"ContinuousAssign({self.assignments})"

class NetDeclaration(ASTNode):
    """网络声明（兼容性）"""
    def __init__(self, net_type, range_spec, names):
        self.net_type = net_type
        self.range_spec = range_spec
        self.names = names

    def __repr__(self):
        return f"NetDeclaration({self.net_type}, {self.range_spec}, {self.names})"

class AlwaysConstruct(ASTNode):
    """always块（兼容性）"""
    def __init__(self, event_control, statements):
        self.event_control = event_control
        self.statements = statements

    def __repr__(self):
        return f"AlwaysConstruct({self.event_control}, {self.statements})"

class EventControl(ASTNode):
    """事件控制（兼容性）"""
    def __init__(self, event_expression):
        self.event_expression = event_expression

    def __repr__(self):
        return f"EventControl({self.event_expression})"

class EventExpression(ASTNode):
    """事件表达式（兼容性）"""
    def __init__(self, edge_type, expression):
        self.edge_type = edge_type
        self.expression = expression

    def __repr__(self):
        return f"EventExpression({self.edge_type}, {self.expression})"

# 测试台相关节点

class TestbenchDeclaration(ASTNode):
    """测试台声明"""
    def __init__(self, module_name, parameters, body):
        self.module_name = module_name  # 被测模块名
        self.parameters = parameters or []  # 测试台参数
        self.body = body or []  # 测试台主体

    def __repr__(self):
        return f"TestbenchDeclaration({self.module_name}, {self.parameters}, {self.body})"

class ClockDeclaration(ASTNode):
    """时钟声明"""
    def __init__(self, clock_name, period):
        self.clock_name = clock_name
        self.period = period

    def __repr__(self):
        return f"ClockDeclaration({self.clock_name}, {self.period})"

class SignalDeclaration(ASTNode):
    """测试信号声明"""
    def __init__(self, signal_name, signal_type, range_spec=None, initial_value=None):
        self.signal_name = signal_name
        self.signal_type = signal_type  # 'wire' or 'reg'
        self.range_spec = range_spec
        self.initial_value = initial_value

    def __repr__(self):
        return f"SignalDeclaration({self.signal_name}, {self.signal_type}, {self.range_spec}, {self.initial_value})"

class DutInstantiation(ASTNode):
    """被测模块实例化"""
    def __init__(self, instance_name, module_name, parameters, port_connections):
        self.instance_name = instance_name
        self.module_name = module_name
        self.parameters = parameters or []
        self.port_connections = port_connections or []

    def __repr__(self):
        return f"DutInstantiation({self.instance_name}, {self.module_name}, {self.parameters}, {self.port_connections})"

class TestSequence(ASTNode):
    """测试序列"""
    def __init__(self, statements):
        self.statements = statements or []

    def __repr__(self):
        return f"TestSequence({self.statements})"

class WaitStatement(ASTNode):
    """等待语句"""
    def __init__(self, duration):
        self.duration = duration

    def __repr__(self):
        return f"WaitStatement({self.duration})"

class DumpWavesStatement(ASTNode):
    """波形输出语句"""
    def __init__(self, filename):
        self.filename = filename

    def __repr__(self):
        return f"DumpWavesStatement({self.filename})"

class ReportCoverageStatement(ASTNode):
    """覆盖率报告语句"""
    def __init__(self):
        pass

    def __repr__(self):
        return "ReportCoverageStatement()"

class ParameterAssignment(ASTNode):
    """参数赋值"""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"ParameterAssignment({self.name}, {self.value})"