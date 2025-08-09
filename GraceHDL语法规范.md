# GraceHDL 语法规范

基于您提供的语法风格，这里是完整的 GraceHDL 语法规范定义。

## 1. 基本语法结构

### 1.1 模块定义
```ghdl
module module_name:
    input(
        # 输入端口定义
    )
    output(
        # 输出端口定义
    )
    register(
        # 寄存器定义
    )
    parameter(
        # 参数定义
    )
    
    # 逻辑块
```

### 1.2 端口定义语法
```ghdl
# 单比特信号
wire signal_name

# 多比特信号
wire(width-1:0) signal_name
wire(7:0) data_bus    # 8位数据总线

# 示例
input(
    wire clk,
    wire rst,
    wire(7:0) data_in,
    wire(15:0) address
)

output(
    wire ready,
    wire(7:0) data_out
)
```

### 1.3 寄存器定义语法
```ghdl
register(
    reg signal_name,                    # 单比特寄存器
    reg(width-1:0) signal_name,        # 多比特寄存器
    reg(7:0) memory[size-1:0]          # 存储器数组
)

# 示例
register(
    reg(7:0) counter,
    reg(1:0) state,
    reg(7:0) buffer[15:0]
)
```

### 1.4 参数定义语法
```ghdl
parameter(
    PARAM_NAME = value,
    WIDTH = 8,
    DEPTH = 256
)
```

## 2. 逻辑块语法

### 2.1 时钟驱动逻辑 (run 块)
```ghdl
# 上升沿触发
run (clk.posedge):
    # 同步逻辑

# 下降沿触发
run (clk.negedge):
    # 同步逻辑

# 多条件触发
run (clk.posedge and rst.negedge):
    # 带异步复位的同步逻辑
```

### 2.2 组合逻辑 (always 块)
```ghdl
always:
    # 组合逻辑
    output = input1 and input2
    result = a + b
```

### 2.3 条件语句
```ghdl
# if-elif-else 语句
if condition:
    # 语句
elif another_condition:
    # 语句
else:
    # 语句

# case 语句
case variable:
    value1:
        # 语句
    value2:
        # 语句
    default:
        # 默认语句
```

## 3. 数据类型和操作符

### 3.1 数据类型
- `wire`: 连线类型，用于组合逻辑
- `reg`: 寄存器类型，用于时序逻辑

### 3.2 位宽表示
```ghdl
wire(7:0) data      # 8位宽度 [7:0]
wire(15:0) address  # 16位宽度 [15:0]
```

### 3.3 常数表示
```ghdl
8'b10101010         # 8位二进制
8'h55               # 8位十六进制
8'd85               # 8位十进制
```

### 3.4 操作符
```ghdl
# 逻辑操作符
and, or, xor, not

# 算术操作符
+, -, *, /

# 比较操作符
==, !=, <, >, <=, >=

# 位操作符
<<, >>              # 移位
&, |, ^, ~          # 按位操作

# 位选择
signal[bit]         # 单比特选择
signal[high:low]    # 位范围选择
```

## 4. 高级语法特性

### 4.1 存储器定义
```ghdl
register(
    reg(7:0) memory[255:0]    # 256个8位存储单元
)

# 访问
memory[address] = data      # 写入
data = memory[address]      # 读取
```

### 4.2 并发赋值
```ghdl
# 在 always 块中的并发赋值
always:
    output1 = input1 and input2
    output2 = input3 or input4
```

### 4.3 时序控制
```ghdl
# 边沿检测
clk.posedge         # 上升沿
clk.negedge         # 下降沿

# 复合条件
run (clk.posedge and rst.negedge):
    if rst:
        # 异步复位
    else:
        # 正常时序逻辑
```

## 5. 语法风格特点

### 5.1 结构化设计
- 清晰的模块结构分离
- 输入、输出、寄存器分别定义
- 逻辑块明确分类

### 5.2 可读性优化
- 使用缩进表示层次结构
- 中文注释支持
- 直观的操作符命名

### 5.3 类型安全
- 明确的位宽定义
- 区分 wire 和 reg 类型
- 编译时类型检查

## 6. 示例模块

### 6.1 简单加法器
```ghdl
module adder_8bit:
    input(
        wire(7:0) a,
        wire(7:0) b,
        wire cin
    )
    output(
        wire(7:0) sum,
        wire cout
    )
    register(
        # 组合逻辑不需要寄存器
    )
    
    always:
        {cout, sum} = a + b + cin
```

### 6.2 D触发器
```ghdl
module d_flip_flop:
    input(
        wire clk,
        wire rst,
        wire d
    )
    output(
        wire q,
        wire qn
    )
    register(
        reg q_reg
    )
    
    run (clk.posedge):
        if rst:
            q_reg = 0
        else:
            q_reg = d
    
    always:
        q = q_reg
        qn = not q_reg
```

## 7. 编译指导

### 7.1 文件扩展名
- `.ghdl` - GraceHDL 源文件

### 7.2 编译命令
```bash
python gracehdl_compiler.py input.ghdl -v
```

### 7.3 输出格式
- 生成标准 Verilog HDL 代码
- 保持原有的逻辑结构
- 优化的代码格式

这种语法设计的优势：
1. **直观易读**：结构清晰，层次分明
2. **类型安全**：明确的类型定义和位宽控制
3. **功能完整**：支持组合逻辑、时序逻辑、状态机等
4. **易于学习**：语法简洁，符合直觉
5. **工程友好**：支持大规模设计和模块化开发