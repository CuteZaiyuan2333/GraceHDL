# GraceHDL 语法规范 v2.0

基于最新的语法优化和功能扩展，这里是完整的 GraceHDL 语法规范定义。

## 📋 目录
1. [基本语法结构](#1-基本语法结构)
2. [数据类型和位宽表示](#2-数据类型和位宽表示)
3. [逻辑块语法](#3-逻辑块语法)
4. [操作符和表达式](#4-操作符和表达式)
5. [高级语法特性](#5-高级语法特性)
6. [扩展功能语法](#6-扩展功能语法)
7. [语法风格特点](#7-语法风格特点)
8. [示例模块](#8-示例模块)

---

## 1. 基本语法结构

### 1.1 模块定义
```ghdl
module module_name:
    parameter(
        # 参数定义
    )
    input(
        # 输入端口定义
    )
    output(
        # 输出端口定义
    )
    register(
        # 寄存器定义
    )
    
    # 逻辑块
```

### 1.2 端口定义语法
```ghdl
# 单比特信号
wire signal_name

# 多比特信号 - 使用 to 语句
wire(width-1 to 0) signal_name
wire(7 to 0) data_bus    # 8位数据总线

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
    reg(width-1, 0) signal_name,       # 多比特寄存器
    reg(7, 0) memory[size-1, 0]        # 存储器数组
)

# 多时钟域寄存器
register(
    reg(7, 0) data_reg clocked_by clk_a,
    reg(7, 0) sync_reg clocked_by clk_b
)

# 示例
register(
    reg(7, 0) counter,
    reg(1, 0) state,
    reg(7, 0) buffer[15, 0]
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

---

## 2. 数据类型和位宽表示

### 2.1 数据类型
- `wire`: 连线类型，用于组合逻辑
- `reg`: 寄存器类型，用于时序逻辑

### 2.2 位宽表示 - 使用逗号分隔
```ghdl
wire(7, 0) data      # 8位宽度 [7:0]
wire(15, 0) address  # 16位宽度 [15:0]
reg(31, 0) register  # 32位寄存器
```

### 2.3 数组表示
```ghdl
# 一维数组
wire(7, 0) data_array[15, 0]    # 16个8位元素
reg(31, 0) registers[255, 0]    # 256个32位寄存器

# 多维数组 - Python风格
memory = [[0] * cols] * rows        # 二维数组
cache = [0] * 1024                  # 一维数组
```

### 2.4 常数表示
```ghdl
# 简化的数值表示
0b10101010      # 二进制
0x55            # 十六进制
85              # 十进制
0               # 零值（编译器自动推断位宽）
```

---

## 3. 逻辑块语法

### 3.1 时钟驱动逻辑 (run 块)
```ghdl
# 上升沿触发 - 统一使用 .posedge
run(clk.posedge):
    # 同步逻辑

# 下降沿触发 - 统一使用 .negedge
run(clk.negedge):
    # 同步逻辑

# 多条件触发
run(clk.posedge and rst.negedge):
    # 带异步复位的同步逻辑
```

### 3.2 组合逻辑 (always 块)
```ghdl
always:
    # 组合逻辑
    output = input1 and input2
    result = a + b
```

### 3.3 连续赋值 (assign 块)
```ghdl
assign:
    # 连续赋值语句
    output = input1 and input2
    sum = a + b + cin
    
    # 归约运算符
    parity = reduce_xor(data)
    all_ones = reduce_and(mask)
```

### 3.4 条件语句
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

### 3.5 For循环生成语句
```ghdl
# For循环生成语句 - 用于重复硬件结构生成
for i in range(start, end):
    # 生成重复的硬件结构
    
# 带步长的For循环
for i in range(start, end, step):
    # 生成语句

# 示例：生成多个寄存器
for i in range(0, 8):
    register(
        reg data_reg[i]
    )
```

---

## 4. 操作符和表达式

### 4.1 逻辑操作符
```ghdl
and, or, xor, not
```

### 4.2 算术操作符
```ghdl
+, -, *, /
```

### 4.3 比较操作符
```ghdl
==, !=, <, >, <=, >=
```

### 4.4 位操作符 - Python风格
```ghdl
# 位选择 - 使用切片语法
signal[7, 0]        # 位范围选择
signal[3]           # 单比特选择

# 位拼接 - 使用 + 运算符
result = a + b      # 位拼接

# 位重复 - 使用 * 运算符
result = a * 4      # 重复4次

# 传统位操作
<<, >>              # 移位
&, |, ^, ~          # 按位操作
```

### 4.5 赋值操作符
```ghdl
# 组合逻辑赋值 - 使用等号
output = input1 and input2
result = a + b

# 时序逻辑赋值 - 使用 to 语句替代 <=
run(clk.posedge):
    (counter + 1) to counter    # 替代 counter <= counter + 1
    data_in to data_reg         # 替代 data_reg <= data_in
    
    # 条件赋值
    if reset:
        0 to counter            # 替代 counter <= 0
    else:
        (counter + 1) to counter  # 替代 counter <= counter + 1

# 多重赋值
run(clk.posedge):
    data_in to reg_a
    reg_a to reg_b
    reg_b to reg_c
```

### 4.6 逻辑蕴含
```ghdl
# 使用 implies 关键字替代箭头
assert(reset implies (count == 0), "Reset assertion failed")
```

---

## 5. 高级语法特性

### 5.1 参数化模块系统
```ghdl
module parameterized_adder:
    parameter(
        WIDTH = 8,
        PIPELINE_STAGES = 2
    )
    input(
        wire clk,
        wire(WIDTH-1, 0) a,
        wire(WIDTH-1, 0) b
    )
    output(
        wire(WIDTH, 0) sum
    )
    
    # 参数化逻辑
    register(
        reg(WIDTH, 0) pipeline[PIPELINE_STAGES-1, 0]
    )
```

### 5.2 枚举类型系统
```ghdl
enum State:
    IDLE = 0
    FETCH = 1
    DECODE = 2
    EXECUTE = 3

module state_machine:
    register(
        State current_state,
        State next_state
    )
    
    run(clk.posedge):
        if reset:
            current_state = State.IDLE
        else:
            current_state = next_state
    
    always:
        case current_state:
            State.IDLE:
                next_state = State.FETCH
            State.FETCH:
                next_state = State.DECODE
            # ...
```

### 5.3 函数定义系统 - Python风格
```ghdl
# 函数定义
def add(x, y):
    return x + y

def parity_check(data):
    result = 0
    for i in range(8):
        result = result xor data[i]
    return result

module calculator:
    input(
        wire(7, 0) a,
        wire(7, 0) b
    )
    output(
        wire(8, 0) sum,
        wire parity
    )
    
    always:
        sum = add(a, b)
        parity = parity_check(a)
```

### 5.4 高级数组操作 - Python风格
```ghdl
module memory_controller:
    parameter(
        SIZE = 1024
    )
    
    register(
        # Python风格数组声明
        memory = [0] * SIZE,
        cache = [[0] * 8] * 16
    )
    
    always:
        # 数组访问
        data_out = memory[address]
        cache_line = cache[index]
```

---

## 6. 扩展功能语法

### 6.1 接口定义系统
```ghdl
interface AXI4_Lite:
    parameter(
        ADDR_WIDTH = 32,
        DATA_WIDTH = 32
    )
    
    input(
        wire(ADDR_WIDTH-1, 0) awaddr,
        wire awvalid
    )
    output(
        wire awready,
        wire(1, 0) bresp
    )

module axi_slave:
    port axi: AXI4_Lite(ADDR_WIDTH=32, DATA_WIDTH=32)
    
    always:
        axi.awready = 1
        axi.bresp = 0b00  # OKAY response
```

### 6.2 生成块扩展
```ghdl
module parallel_processor:
    parameter(
        NUM_CORES = 4,
        DATA_WIDTH = 32
    )
    
    generate:
        for i in range(NUM_CORES):
            processing_unit core_inst:
                .clk(clk)
                .data_in(data_in[i])
                .data_out(data_out[i])
                .core_id(i)
```

### 6.3 多时钟域支持
```ghdl
module clock_domain_crossing:
    input(
        wire clk_a,
        wire clk_b,
        wire(7, 0) data_in
    )
    
    register(
        reg(7, 0) data_reg clocked_by clk_a,
        reg(7, 0) sync_reg1 clocked_by clk_b,
        reg(7, 0) sync_reg2 clocked_by clk_b
    )
    
    run(clk_a.posedge):
        data_in to data_reg
    
    run(clk_b.posedge):
        data_reg to sync_reg1
        sync_reg1 to sync_reg2
```

### 6.4 断言系统
```ghdl
module counter_with_assertions:
    parameter(
        WIDTH = 8,
        MAX_COUNT = 255
    )
    
    register(
        reg(WIDTH-1, 0) counter_reg
    )
    
    run(clk.posedge):
        if reset:
            0 to counter_reg
        else:
            (counter_reg + 1) to counter_reg
    
    always:
        # 功能断言
        assert(counter_reg <= MAX_COUNT, "Counter overflow detected")
        
        # 时序断言
        assert(reset implies (count == 0), "Reset assertion failed")
        
        # 覆盖率断言
        cover(counter_reg == MAX_COUNT, "Maximum count reached")
```

### 6.5 测试台自动生成
```ghdl
testbench for counter:
    parameter(
        CLK_PERIOD = 10ns,
        TEST_CYCLES = 100
    )
    
    # 自动生成时钟
    clock clk with period CLK_PERIOD
    
    # 测试信号
    signal reset: wire = 0
    signal count: wire(7, 0)
    
    # 被测模块实例化
    dut: counter(WIDTH=8, MAX_COUNT=255)
        .clk(clk)
        .reset(reset)
        .count(count)
    
    # 测试序列
    test_sequence:
        reset = 1
        wait for 2 * CLK_PERIOD
        assert(count == 0, "Reset test failed")
        
        reset = 0
        wait for TEST_CYCLES * CLK_PERIOD
        assert(count == TEST_CYCLES, "Count test failed")
    
    # 波形输出
    dump_waves to "counter_test.vcd"
    
    # 测试报告
    report_coverage
```

---

## 7. 语法风格特点

### 7.1 Python风格优化
- **简洁性**: 减少符号使用，使用自然语言关键字
- **赋值优化**: 使用 `to` 语句替代 `<=` 进行时序赋值
- **直观性**: 使用 `.posedge/.negedge` 统一边沿检测
- **易读性**: 使用 `implies`, `wait for`, `clocked_by` 等自然语言

### 7.2 结构化设计
- 清晰的模块结构分离
- 输入、输出、寄存器分别定义
- 逻辑块明确分类

### 7.3 类型安全
- 明确的位宽定义
- 区分 wire 和 reg 类型
- 编译时类型检查和推断

### 7.4 生成语句设计理念
- **硬件生成导向**: For循环专门用于生成重复的硬件结构
- **编译时展开**: 所有For循环在编译时完全展开
- **参数化设计**: 支持使用参数控制生成的硬件规模
- **层次化生成**: 支持嵌套For循环生成复杂硬件阵列

---

## 8. 示例模块

### 8.1 简单加法器
```ghdl
module adder_8bit:
    input(
        wire(7, 0) a,
        wire(7, 0) b,
        wire cin
    )
    output(
        wire(7, 0) sum,
        wire cout
    )
    
    assign:
        {cout, sum} = a + b + cin
```

### 8.2 参数化计数器
```ghdl
module parameterized_counter:
    parameter(
        WIDTH = 8,
        MAX_COUNT = 255
    )
    input(
        wire clk,
        wire reset,
        wire enable
    )
    output(
        wire(WIDTH-1, 0) count,
        wire overflow
    )
    
    register(
        reg(WIDTH-1, 0) counter_reg
    )
    
    run(clk.posedge):
        if reset:
            0 to counter_reg
        elif enable:
            if counter_reg == MAX_COUNT:
                0 to counter_reg
            else:
                (counter_reg + 1) to counter_reg
    
    always:
        count = counter_reg
        overflow = (counter_reg == MAX_COUNT) and enable
```

### 8.3 状态机示例
```ghdl
enum TrafficState:
    RED = 0
    YELLOW = 1
    GREEN = 2

module traffic_light:
    parameter(
        RED_TIME = 100,
        YELLOW_TIME = 20,
        GREEN_TIME = 80
    )
    
    input(
        wire clk,
        wire reset
    )
    output(
        wire red_light,
        wire yellow_light,
        wire green_light
    )
    
    register(
        TrafficState current_state,
        reg(7, 0) timer
    )
    
    run(clk.posedge):
        if reset:
            TrafficState.RED to current_state
            0 to timer
        else:
            case current_state:
                TrafficState.RED:
                    if timer == RED_TIME:
                        TrafficState.GREEN to current_state
                        0 to timer
                    else:
                        (timer + 1) to timer
                
                TrafficState.GREEN:
                    if timer == GREEN_TIME:
                        TrafficState.YELLOW to current_state
                        0 to timer
                    else:
                        (timer + 1) to timer
                
                TrafficState.YELLOW:
                    if timer == YELLOW_TIME:
                        TrafficState.RED to current_state
                        0 to timer
                    else:
                        (timer + 1) to timer
    
    always:
        red_light = (current_state == TrafficState.RED)
        yellow_light = (current_state == TrafficState.YELLOW)
        green_light = (current_state == TrafficState.GREEN)
```

### 8.4 使用函数的ALU
```ghdl
def add_func(a, b):
    return a + b

def sub_func(a, b):
    return a - b

def and_func(a, b):
    return a and b

module alu:
    parameter(
        WIDTH = 8
    )
    
    input(
        wire(WIDTH-1, 0) a,
        wire(WIDTH-1, 0) b,
        wire(1, 0) op_code
    )
    output(
        wire(WIDTH-1, 0) result
    )
    
    always:
        case op_code:
            0:
                result = add_func(a, b)
            1:
                result = sub_func(a, b)
            2:
                result = and_func(a, b)
            default:
                result = 0
```

---

## 9. 编译指导

### 9.1 文件扩展名
- `.ghdl` - GraceHDL 源文件

### 9.2 编译命令
```bash
python gracehdl_compiler.py input.ghdl -v
```

### 9.3 输出格式
- 生成标准 Verilog HDL 代码
- 保持原有的逻辑结构
- 优化的代码格式

---

## 10. 语法优势总结

### 10.1 学习友好性
- **Python风格**: 熟悉的语法降低学习门槛
- **自然语言**: 使用直观的关键字和表达式
- **简洁明了**: 减少复杂符号，提高可读性

### 10.2 功能完整性
- **全面覆盖**: 支持所有Verilog核心功能
- **扩展能力**: 提供高级抽象和生成能力
- **类型安全**: 编译时类型检查和推断

### 10.3 工程实用性
- **模块化设计**: 支持大规模项目开发
- **参数化**: 灵活的硬件配置能力
- **验证支持**: 内置断言和测试台生成

### 10.4 创新特性
- **生成语句**: 强大的硬件生成能力
- **多时钟域**: 现代设计需求支持
- **接口定义**: 标准化接口设计

这种语法设计使GraceHDL成为一个既易学又强大的硬件描述语言，特别适合教学和快速原型开发。