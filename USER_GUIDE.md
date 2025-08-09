# GraceHDL 用户指南

## 目录
1. [快速开始](#快速开始)
2. [语法详解](#语法详解)
3. [示例教程](#示例教程)
4. [编译器使用](#编译器使用)
5. [常见问题](#常见问题)

## 快速开始

### 环境准备

1. 确保已安装 Python 3.7+
2. 安装依赖包：
```bash
pip install -r requirements.txt
```

### 第一个程序

创建文件 `hello.ghdl`：

```gracehdl
module hello_world:
    input(wire clk)
    output(reg led)
    register(reg counter)
    
    run (clk.posedge):
        counter = counter + (1, d, 1)
    
    always:
        led = counter
```

编译为 Verilog：

```bash
python gracehdl_compiler.py hello.ghdl -o hello.v
```

## 语法详解

### 模块定义

GraceHDL 使用清晰的结构化语法定义模块：

```gracehdl
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
        # 参数定义（可选）
    )
    
    # 逻辑块
```

### 端口声明

#### 基本语法
```gracehdl
# 单比特信号
wire signal_name
reg register_name

# 多比特信号  
wire(width-1:0) bus_name
reg(7:0) data_reg
```

#### 示例
```gracehdl
input(
    wire clk,           # 时钟信号
    wire reset,         # 复位信号
    wire(7:0) data_in,  # 8位数据输入
    wire(15:0) addr     # 16位地址
)

output(
    wire ready,         # 就绪信号
    reg(7:0) data_out   # 8位数据输出
)

register(
    reg(7:0) counter,   # 8位计数器
    reg(1:0) state      # 2位状态寄存器
)
```

### 数值格式

GraceHDL 使用新的数值格式 `(value, base, width)`：

```gracehdl
(0, d, 8)      # 8位十进制0
(255, d, 8)    # 8位十进制255
(0, b, 4)      # 4位二进制0
(15, h, 4)     # 4位十六进制F
(7, o, 3)      # 3位八进制7
```

### 逻辑块

#### 时序逻辑 (run 块)
用于描述在时钟边沿触发的逻辑：

```gracehdl
# 上升沿触发
run (clk.posedge):
    if reset:
        counter = (0, d, 8)
    else:
        counter = counter + (1, d, 8)

# 下降沿触发  
run (clk.negedge):
    output_reg = input_signal
```

#### 组合逻辑 (always 块)
用于描述组合逻辑：

```gracehdl
always:
    output = input1 & input2
    result = a + b
    ready = (counter == (255, d, 8))
```

### 控制结构

#### if-else 语句
```gracehdl
if condition:
    # 语句
elif another_condition:
    # 语句  
else:
    # 语句
```

#### case 语句
```gracehdl
case variable:
    (0, d, 2):
        # 当 variable == 0 时
        state = (1, d, 2)
    (1, d, 2):
        # 当 variable == 1 时
        state = (2, d, 2)
    default:
        # 默认情况
        state = (0, d, 2)
```

## 示例教程

### 示例1: 简单计数器

```gracehdl
module simple_counter:
    input(wire clk, wire reset)
    output(reg(7:0) count)
    register(reg(7:0) count_reg)
    
    run (clk.posedge):
        if reset:
            count_reg = (0, d, 8)
        else:
            count_reg = count_reg + (1, d, 8)
    
    always:
        count = count_reg
```

**说明**:
- `run (clk.posedge)`: 在时钟上升沿执行
- `if reset`: 复位时将计数器清零
- `else`: 正常情况下计数器加1
- `always`: 将内部寄存器值输出

### 示例2: 状态机

```gracehdl
module traffic_light:
    input(wire clk, wire reset)
    output(reg(1:0) light)
    register(reg(1:0) state, reg(7:0) timer)
    
    run (clk.posedge):
        if reset:
            state = (0, d, 2)
            timer = (0, d, 8)
        else:
            case state:
                (0, d, 2):  # 红灯状态
                    if timer == (50, d, 8):
                        state = (1, d, 2)
                        timer = (0, d, 8)
                    else:
                        timer = timer + (1, d, 8)
                (1, d, 2):  # 绿灯状态
                    if timer == (30, d, 8):
                        state = (2, d, 2)
                        timer = (0, d, 8)
                    else:
                        timer = timer + (1, d, 8)
                (2, d, 2):  # 黄灯状态
                    if timer == (10, d, 8):
                        state = (0, d, 2)
                        timer = (0, d, 8)
                    else:
                        timer = timer + (1, d, 8)
                default:
                    state = (0, d, 2)
    
    always:
        light = state
```

**说明**:
- 三状态交通灯控制器
- 使用计时器控制状态转换
- 红灯50个时钟周期，绿灯30个，黄灯10个

### 示例3: 算术逻辑单元 (ALU)

```gracehdl
module simple_alu:
    input(wire(7:0) a, wire(7:0) b, wire(1:0) op)
    output(reg(7:0) result)
    
    always:
        case op:
            (0, d, 2):  # 加法
                result = a + b
            (1, d, 2):  # 减法
                result = a - b
            (2, d, 2):  # 与运算
                result = a & b
            (3, d, 2):  # 或运算
                result = a | b
            default:
                result = (0, d, 8)
```

## 编译器使用

### 命令行工具

基本用法：
```bash
python gracehdl_compiler.py input.ghdl [-o output.v]
```

参数说明：
- `input.ghdl`: 输入的 GraceHDL 文件
- `-o output.v`: 指定输出的 Verilog 文件（可选）

### 编程接口

```python
from src.compiler import GraceHDLCompiler

compiler = GraceHDLCompiler()

# 编译文件
success = compiler.compile_file('input.ghdl', 'output.v')

# 编译字符串
verilog_code = compiler.compile_string(gracehdl_source)
```

### 生成的 Verilog 代码

GraceHDL 编译器生成标准的 Verilog 代码，可以直接用于：
- 仿真工具 (ModelSim, VCS, Icarus Verilog)
- 综合工具 (Vivado, Quartus, Yosys)
- FPGA 开发流程

## 常见问题

### Q: 数值格式 `(value, base, width)` 中的 base 参数有哪些选项？

A: 支持以下进制：
- `d`: 十进制 (decimal)
- `b`: 二进制 (binary)  
- `h`: 十六进制 (hexadecimal)
- `o`: 八进制 (octal)

### Q: 如何表示多位宽的信号？

A: 使用 `(high:low)` 格式：
```gracehdl
wire(7:0) data_bus    # 8位总线，位7到位0
reg(15:0) address     # 16位地址寄存器
```

### Q: run 块和 always 块的区别是什么？

A: 
- `run` 块：用于时序逻辑，在时钟边沿触发
- `always` 块：用于组合逻辑，输入变化时立即更新

### Q: 编译出错时如何调试？

A: 
1. 检查语法是否正确（冒号、括号、缩进）
2. 确认数值格式是否使用新格式 `(value, base, width)`
3. 查看错误信息中的 token 类型，定位语法问题
4. 参考 `examples/` 目录中的正确示例

### Q: 支持哪些操作符？

A: 当前支持：
- 算术：`+`, `-`, `*`, `/`
- 逻辑：`&`, `|`, `^`, `~`
- 比较：`==`, `!=`, `<`, `>`, `<=`, `>=`
- 赋值：`=`

### Q: 如何查看生成的 Verilog 代码？

A: 编译成功后，Verilog 代码会保存到指定的输出文件中。可以用任何文本编辑器查看。

---

更多示例和详细信息请参考：
- [语法规范](GraceHDL语法规范.md)
- [开发进度](DEVELOPMENT_PROGRESS.md)
- [示例代码](examples/)