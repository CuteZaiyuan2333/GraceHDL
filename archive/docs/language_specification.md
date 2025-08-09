# GraceHDL语言规范

## 概述

GraceHDL是一种现代化的硬件描述语言，旨在提供简洁、易读的语法来描述数字电路。它使用Python风格的缩进和换行来替代传统的分号和大括号，让硬件设计更加直观。

## 语法特性

### 1. 缩进语法

GraceHDL使用缩进来表示代码块的层次结构，而不是使用大括号：

```gracehdl
module example
    input wire clk
    output reg data
    
    always @(posedge clk)
        if reset
            data <= 0
        else
            data <= data + 1
```

### 2. 换行分隔

语句之间使用换行分隔，而不是分号：

```gracehdl
assign a = b & c
assign d = e | f
assign g = h ^ i
```

### 3. 模块定义

模块定义语法简洁明了：

```gracehdl
module module_name #(parameter PARAM = value)
    input wire[7:0] input_port
    output reg[7:0] output_port
    
    // 模块内容
```

## 数据类型

### 1. 基本类型

- `wire`: 连线类型，用于组合逻辑
- `reg`: 寄存器类型，用于时序逻辑

### 2. 位宽声明

```gracehdl
wire[7:0] data_bus      // 8位数据总线
reg[15:0] address       // 16位地址寄存器
wire single_bit         // 单比特信号
```

### 3. 数字表示

```gracehdl
8'b10101010            // 8位二进制数
16'hABCD               // 16位十六进制数
8'd255                 // 8位十进制数
32                     // 十进制数
```

## 运算符

### 1. 算术运算符

- `+`: 加法
- `-`: 减法
- `*`: 乘法
- `/`: 除法
- `%`: 取模

### 2. 逻辑运算符

- `&`: 按位与
- `|`: 按位或
- `^`: 按位异或
- `~`: 按位取反
- `&&`: 逻辑与
- `||`: 逻辑或
- `!`: 逻辑非

### 3. 比较运算符

- `==`: 等于
- `!=`: 不等于
- `<`: 小于
- `<=`: 小于等于
- `>`: 大于
- `>=`: 大于等于

### 4. 移位运算符

- `<<`: 左移
- `>>`: 右移

## 语句类型

### 1. 连续赋值

```gracehdl
assign output = input1 & input2
assign result = condition ? true_value : false_value
```

### 2. 过程赋值

#### 阻塞赋值
```gracehdl
always @(*)
    result = a + b
```

#### 非阻塞赋值
```gracehdl
always @(posedge clk)
    counter <= counter + 1
```

### 3. 条件语句

```gracehdl
if condition
    statement1
elsif another_condition
    statement2
else
    statement3
```

### 4. 选择语句

```gracehdl
case selector
    2'b00:
        output = input_a
    2'b01:
        output = input_b
    2'b10:
        output = input_c
    default:
        output = 0
```

### 5. 循环语句

#### for循环
```gracehdl
for i = 0; i < 8; i = i + 1
    array[i] = 0
```

#### while循环
```gracehdl
while counter < limit
    counter = counter + 1
```

## 时序控制

### 1. 时钟边沿

```gracehdl
always @(posedge clk)        // 上升沿
always @(negedge clk)        // 下降沿
always @(posedge clk or posedge reset)  // 多个事件
```

### 2. 组合逻辑

```gracehdl
always @(*)                  // 敏感列表自动推导
always @(a or b or c)        // 显式敏感列表
```

## 模块实例化

### 1. 位置连接

```gracehdl
counter_module counter_inst(clk, reset, count_out)
```

### 2. 命名连接

```gracehdl
counter_module counter_inst(
    .clk(system_clock),
    .reset(system_reset),
    .count(counter_output)
)
```

### 3. 参数化实例

```gracehdl
memory_module #(8, 256) mem_inst(
    .clk(clk),
    .addr(address),
    .data(data_bus)
)
```

## 参数和常量

### 1. 参数定义

```gracehdl
module parameterized_module #(
    parameter WIDTH = 8,
    parameter DEPTH = 256
)
    input wire[WIDTH-1:0] data_in
    output reg[WIDTH-1:0] data_out
```

### 2. 局部参数

```gracehdl
module example
    localparam STATE_IDLE = 2'b00
    localparam STATE_ACTIVE = 2'b01
```

## 注释

```gracehdl
// 单行注释

/*
 * 多行注释
 * 可以跨越多行
 */
```

## 编译指令

GraceHDL代码通过编译器转换为标准Verilog HDL代码：

```bash
python gracehdl_compiler.py input.ghdl -o output.v
```

## 最佳实践

1. **一致的缩进**: 使用4个空格作为缩进单位
2. **清晰的命名**: 使用描述性的变量和模块名
3. **适当的注释**: 为复杂逻辑添加注释
4. **模块化设计**: 将复杂设计分解为小的模块
5. **参数化**: 使用参数提高模块的可重用性

## 与Verilog的对比

| 特性 | GraceHDL | Verilog |
|------|----------|---------|
| 代码块 | 缩进 | begin/end |
| 语句分隔 | 换行 | 分号 |
| 可读性 | 高 | 中等 |
| 学习曲线 | 平缓 | 陡峭 |
| 兼容性 | 转换为Verilog | 原生支持 |