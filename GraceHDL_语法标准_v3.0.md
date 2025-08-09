# GraceHDL 语法标准 v3.0

基于实际demo文件验证的语法和规划功能的完整语法标准定义。

## ⚡ 重要提示：双重赋值语法系统

GraceHDL 提供两种赋值语法，对应不同的硬件语义：

- **`to` 语法**：非阻塞赋值 → `value to reg` 转换为 `reg <= value`（**时序逻辑推荐**）
- **`=` 语法**：阻塞赋值 → `reg = value` 转换为 `reg = value`（组合逻辑或特殊情况）

💡 **最佳实践**：在 `run` 块中优先使用 `to` 语法，确保时序安全！

## 📋 目录
1. [基本语法结构](#1-基本语法结构)
2. [数据类型和位宽表示](#2-数据类型和位宽表示)
3. [逻辑块语法](#3-逻辑块语法)
4. [赋值语法](#4-赋值语法) ⭐
5. [操作符和表达式](#5-操作符和表达式)
6. [控制结构](#6-控制结构)
7. [高级语法特性](#7-高级语法特性)
8. [模块实例化](#8-模块实例化)
9. [语法风格规范](#9-语法风格规范)

---

## 1. 基本语法结构

### 1.1 模块定义
```ghdl
module module_name:
    # 模块内容使用4空格缩进
    input(
        # 输入端口定义
    )
    output(
        # 输出端口定义
    )
    register(
        # 寄存器定义（可选）
    )
    parameter(
        # 参数定义（可选）
    )
    
    # 逻辑块
```

### 1.2 端口定义语法
```ghdl
# 单比特信号
wire signal_name

# 多比特信号 - 使用逗号分隔的位宽表示
wire(high_bit, low_bit) signal_name

# 示例
input(
    wire clk,
    wire rst,
    wire(7, 0) data_in,
    wire(15, 0) address
)

output(
    wire ready,
    wire(7, 0) data_out
)
```

### 1.3 寄存器定义语法
```ghdl
register(
    reg signal_name,                    # 单比特寄存器
    reg(high_bit, low_bit) signal_name, # 多比特寄存器
    reg(width-1, 0) memory[size-1, 0]   # 存储器数组（规划中）
)

# 示例
register(
    reg(7, 0) counter,
    reg(1, 0) state,
    reg q_reg
)
```

### 1.4 参数定义语法（规划中）
```ghdl
parameter(
    PARAM_NAME = value,
    WIDTH = 8,
    DEPTH = 256
)
```

---

## 2. 数据类型和位宽表示

### 2.1 数据类型
- `wire`: 连线类型，用于组合逻辑
- `reg`: 寄存器类型，用于时序逻辑

### 2.2 位宽表示
```ghdl
wire(7, 0) data      # 8位宽度 [7:0]
wire(15, 0) address  # 16位宽度 [15:0]
reg(31, 0) register  # 32位寄存器
```

### 2.3 数值表示
```ghdl
# 新数值格式 (value, base, width)
(0, d, 8)       # 8位十进制0
(255, d, 8)     # 8位十进制255
(0xFF, h, 8)    # 8位十六进制FF
(0b10101010, b, 8)  # 8位二进制

# 简化表示
0               # 零值（编译器自动推断位宽）
1               # 一值（编译器自动推断位宽）
```

### 2.4 位选择和拼接
```ghdl
# 位选择
signal[7]           # 选择第7位
signal[7, 0]        # 选择位段[7:0]
signal[6, 0]        # 选择位段[6:0]

# 位拼接
result = a + b      # 拼接操作
shift_reg = shift_reg[6, 0] + serial_in  # 移位拼接
```

---

## 3. 逻辑块语法

### 3.1 时钟驱动逻辑 (run 块)
```ghdl
# 上升沿触发
run(clk.posedge):
    # 时序逻辑，推荐使用 to 语法（非阻塞赋值）
    if rst:
        0 to counter              # 非阻塞赋值 ← 推荐
        0 to state               # 非阻塞赋值 ← 推荐
    else:
        (counter + 1) to counter  # 非阻塞赋值 ← 推荐
        next_state to state      # 非阻塞赋值 ← 推荐
    
    # 也支持传统 = 语法（阻塞赋值），但需谨慎使用
    # counter = counter + 1     # 阻塞赋值，可能导致时序问题

# 下降沿触发
run(clk.negedge):
    # 同步逻辑，同样推荐使用 to 语法
    data_in to shift_reg

# 多条件触发（规划中）
run(clk.posedge and rst.negedge):
    # 带异步复位的同步逻辑
```

### 3.2 组合逻辑 (always 块)
```ghdl
always:
    # 组合逻辑，使用 = 赋值
    case addr:
        (0, d, 3):
            out = (1, d, 8)
        (1, d, 3):
            out = (2, d, 8)
        default:
            out = (0, d, 8)
```

### 3.3 连续赋值 (assign 块)
```ghdl
assign:
    # 连续赋值语句
    y = a and b
    sum = a xor b xor cin
    cout = (a and b) or (cin and (a xor b))
```

---

## 4. 赋值语法

### 4.1 阻塞赋值语法（= 操作符）
```ghdl
# 在 run 块中使用 = 进行阻塞赋值（转换为 Verilog 的 = ）
run(clk.posedge):
    counter = counter + 1         # 阻塞赋值
    data_reg = data_in           # 阻塞赋值

# 在 always 和 assign 块中使用 = 进行组合赋值
always:
    output = input_a and input_b  # 组合逻辑赋值

assign:
    sum = a + b                  # 连续赋值
```

### 4.2 非阻塞赋值语法（to 操作符）⭐
```ghdl
# 使用 to 语法进行非阻塞赋值，专用于时序逻辑
run(clk.posedge):
    (counter + 1) to counter      # 非阻塞赋值，转换为 Verilog 的 counter <= counter + 1
    data_in to data_reg           # 非阻塞赋值，转换为 Verilog 的 data_reg <= data_in
    0 to reset_counter            # 非阻塞赋值，转换为 Verilog 的 reset_counter <= 0

# ⚠️ 重要：to 语法只能在 run 块中使用，不能在 always 或 assign 块中使用
```

### 4.3 赋值语法特性对比
| 赋值类型 | GraceHDL 语法 | Verilog 转换 | 执行特性 | 推荐使用场景 |
|----------|---------------|-------------|----------|-------------|
| **非阻塞赋值** | `value to reg` | `reg <= value` | 并行执行，时序安全 | **时序逻辑（推荐）** |
| 阻塞赋值 | `reg = value` | `reg = value` | 顺序执行 | 组合逻辑或特殊情况 |
| 组合赋值 | `wire = value` | `assign wire = value` | 连续赋值 | always/assign 块 |

### 4.4 赋值语法选择指南
```ghdl
# ✅ 推荐：时序逻辑使用 to 语法（非阻塞）
run(clk.posedge):
    if rst:
        0 to counter              # 非阻塞赋值
        0 to state               # 非阻塞赋值
    else:
        (counter + 1) to counter  # 非阻塞赋值
        next_state to state      # 非阻塞赋值

# ⚠️ 谨慎使用：时序逻辑中的阻塞赋值
run(clk.posedge):
    temp = data_in               # 阻塞赋值，可能导致时序问题
    temp to output_reg           # 非阻塞赋值

# ✅ 正确：组合逻辑使用 = 语法
always:
    output = input_a and input_b # 组合逻辑赋值

assign:
    sum = a + b                  # 连续赋值
```

---

## 5. 操作符和表达式

### 5.1 逻辑操作符
```ghdl
and     # 逻辑与
or      # 逻辑或
not     # 逻辑非
xor     # 逻辑异或
```

### 5.2 算术操作符
```ghdl
+       # 加法
-       # 减法
*       # 乘法（规划中）
/       # 除法（规划中）
```

### 5.3 比较操作符
```ghdl
==      # 等于
!=      # 不等于
<       # 小于
>       # 大于
<=      # 小于等于
>=      # 大于等于
```

### 5.4 位操作符
```ghdl
~       # 按位取反
&       # 按位与（规划中）
|       # 按位或（规划中）
^       # 按位异或（规划中）
```

---

## 6. 控制结构

### 6.1 条件语句
```ghdl
# if-elif-else 语句
if condition:
    # 语句
elif another_condition:
    # 语句
else:
    # 语句

# 示例
if rst:
    count_reg = 0
elif load:
    count_reg = load_value
elif enable:
    count_reg = count_reg + 1
```

### 6.2 case 语句
```ghdl
case variable:
    value1:
        # 语句
    value2:
        # 语句
    default:
        # 默认语句

# 示例
case addr:
    (0, d, 3):
        out = (1, d, 8)
    (1, d, 3):
        out = (2, d, 8)
    default:
        out = (0, d, 8)
```

---

## 7. 高级语法特性

### 7.1 For循环生成语句（规划中）
```ghdl
# For循环生成语句 - 用于重复硬件结构生成
for i in range(start, end):
    # 生成重复的硬件结构
    
# 示例：生成多个寄存器
for i in range(0, 8):
    register(
        reg data_reg[i]
    )
```

### 7.2 枚举类型（规划中）
```ghdl
enum State:
    IDLE = 0,
    FETCH = 1,
    DECODE = 2,
    EXECUTE = 3

register(
    State current_state
)

run(clk.posedge):
    if reset:
        current_state = State.IDLE
    else:
        case current_state:
            State.IDLE: current_state = State.FETCH
            State.FETCH: current_state = State.DECODE
```

### 7.3 函数定义（规划中）
```ghdl
function add(a: wire(7, 0), b: wire(7, 0)) -> wire(8, 0):
    return a + b

always:
    result = add(operand_a, operand_b)
```

### 7.4 接口定义（规划中）
```ghdl
interface bus_interface:
    wire(7, 0) data
    wire valid
    wire ready

module processor:
    input(
        wire clk,
        wire rst
    )
    bus_interface.master cpu_bus
```

---

## 8. 模块实例化

### 8.1 基本实例化语法
```ghdl
module top_module:
    input(
        wire clk,
        wire rst,
        wire(7, 0) data_in
    )
    output(
        wire(7, 0) data_out
    )
    
    # 实例化子模块
    counter_8bit counter_inst:
        .clk(clk),
        .rst(rst),
        .enable(1),
        .count(data_out)
```

### 8.2 参数化实例化（规划中）
```ghdl
parameterized_counter #(
    .WIDTH(16),
    .MAX_COUNT(65535)
) counter_16bit_inst:
    .clk(clk),
    .rst(rst),
    .enable(enable),
    .count(count_16)
```

---

## 9. 语法风格规范

### 9.1 缩进规范
- 使用4个空格进行缩进
- 模块内的所有块（input、output、register等）相对于module关键字缩进4个空格
- 块内的语句相对于块关键字再缩进4个空格

### 9.2 命名规范
- 模块名：使用小写字母和下划线，如 `counter_8bit`
- 信号名：使用小写字母和下划线，如 `data_in`, `clk_out`
- 参数名：使用大写字母和下划线，如 `WIDTH`, `MAX_COUNT`

### 9.3 注释规范
```ghdl
# 单行注释
# 多行注释的第一行
# 多行注释的第二行

module example:  # 行内注释
    input(
        wire clk  # 时钟信号
    )
```

### 9.4 代码组织
- 每个模块定义独立成块
- 相关的模块可以放在同一个文件中
- 复杂的设计建议分文件组织

---

## 10. 实际应用示例

### 10.1 基本门电路
```ghdl
module and_gate:
    input(
        wire a,
        wire b
    )
    output(
        wire y
    )
    
    assign:
        y = a and b
```

### 10.2 时序逻辑（推荐使用非阻塞赋值）
```ghdl
module d_flip_flop:
    input(
        wire clk,
        wire rst,
        wire d
    )
    output(
        wire q
    )
    
    register(
        reg q_reg
    )
    
    run(clk.posedge):
        if rst:
            0 to q_reg           # 非阻塞赋值 ← 推荐
        else:
            d to q_reg           # 非阻塞赋值 ← 推荐
    
    assign:
        q = q_reg               # 组合逻辑赋值
```

### 10.3 状态机（推荐使用非阻塞赋值）
```ghdl
module traffic_light_controller:
    input(
        wire clk,
        wire rst
    )
    output(
        wire(1, 0) lights
    )
    
    register(
        reg(1, 0) current_state,
        reg(3, 0) counter
    )
    
    run(clk.posedge):
        if rst:
            (0, d, 2) to current_state    # 非阻塞赋值 ← 推荐
            (0, d, 4) to counter          # 非阻塞赋值 ← 推荐
        else:
            if counter == (15, d, 4):
                (0, d, 4) to counter      # 非阻塞赋值 ← 推荐
                case current_state:
                    (0, d, 2): (1, d, 2) to current_state    # 非阻塞赋值
                    (1, d, 2): (2, d, 2) to current_state    # 非阻塞赋值
                    (2, d, 2): (0, d, 2) to current_state    # 非阻塞赋值
                    default: (0, d, 2) to current_state      # 非阻塞赋值
            else:
                (counter + 1) to counter  # 非阻塞赋值 ← 推荐
    
    assign:
        lights = current_state           # 组合逻辑赋值
```

---

## 11. 编译器支持状态

### ✅ 已实现功能
- 基本模块定义和端口声明
- 时序逻辑（run块）和组合逻辑（always块）
- 连续赋值（assign块）
- 条件语句（if-elif-else）和case语句
- 基本数据类型（wire、reg）和位宽支持
- 新数值格式 (value, base, width)
- 位选择和拼接操作
- 基本操作符支持
- **双重赋值语法系统**：
  - `to` 语法：非阻塞赋值（`value to reg` → `reg <= value`）
  - `=` 语法：阻塞赋值（`reg = value` → `reg = value`）

### 🚧 规划中功能
- 参数化模块系统
- For循环生成语句
- 枚举类型系统
- 函数定义系统
- 接口定义系统
- 高级数组操作
- 更多操作符支持

---

## 12. 版本历史

### v3.0 (当前版本)
- 基于实际demo文件验证的语法标准
- 明确区分已实现和规划中的功能
- 统一的语法风格规范
- 完整的应用示例

### v2.x (已归档)
- 早期语法规范版本
- 部分功能规划但未验证
- 已移动到 legacy_docs 文件夹

---

*本文档基于GraceHDL项目的五个demo文件实际语法和其他规划文档编写，确保语法标准的准确性和实用性。*