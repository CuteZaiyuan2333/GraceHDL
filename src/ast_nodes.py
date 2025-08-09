"""
GraceHDL抽象语法树节点定义 - 新语法版本
定义所有AST节点类，用于表示解析后的新GraceHDL语法结构
"""

class ASTNode:
    """AST节点基类"""
    pass

class SourceText(ASTNode):
    """源代码根节点"""
    def __init__(self, modules):
        self.modules = modules

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

class IfStatement(ASTNode):
    """if语句"""
    def __init__(self, condition, then_statements, else_statements=None):
        self.condition = condition
        self.then_statements = then_statements or []
        self.else_statements = else_statements or []

    def __repr__(self):
        return f"IfStatement({self.condition}, {self.then_statements}, {self.else_statements})"

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

class BinaryExpression(Expression):
    """二元表达式"""
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

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