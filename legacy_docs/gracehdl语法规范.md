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

### 2.4 For循环和生成语句
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

# 示例：生成并行加法器
for i in range(0, WIDTH):
    always:
        sum[i] = a[i] xor b[i] xor carry[i]
        carry[i+1] = (a[i] and b[i]) or (carry[i] and (a[i] xor b[i]))
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

### 4.4 For循环生成语句详解
```ghdl
# 1. 数组初始化
for i in range(0, ARRAY_SIZE):
    run (clk.posedge):
        if rst:
            data_array[i] = 0
        else:
            data_array[i] = input_data[i]

# 2. 并行处理单元生成
for i in range(0, PROC_UNITS):
    # 实例化处理单元
    processor_unit proc_inst[i] (
        .clk(clk),
        .data_in(data_in[i]),
        .data_out(data_out[i])
    )

# 3. 存储器阵列生成
for row in range(0, ROWS):
    for col in range(0, COLS):
        register(
            reg memory_cell[row][col]
        )
        
        always:
            if (row_select == row) and (col_select == col):
                memory_cell[row][col] = write_data
            read_data = memory_cell[row_select][col_select]

# 4. 流水线级生成
for stage in range(0, PIPELINE_STAGES):
    register(
        reg(DATA_WIDTH-1:0) pipe_data[stage],
        reg pipe_valid[stage]
    )
    
    run (clk.posedge):
        if rst:
            pipe_data[stage] = 0
            pipe_valid[stage] = 0
        else:
            if stage == 0:
                pipe_data[stage] = input_data
                pipe_valid[stage] = input_valid
            else:
                pipe_data[stage] = pipe_data[stage-1]
                pipe_valid[stage] = pipe_valid[stage-1]

# 5. 总线连接生成
for i in range(0, BUS_WIDTH):
    always:
        if bus_enable:
            bus_out[i] = bus_in[i]
        else:
            bus_out[i] = 1'bz  # 高阻态
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

### 5.4 生成语句设计理念
- **硬件生成导向**：For循环专门用于生成重复的硬件结构，而非软件中的循环执行
- **编译时展开**：所有For循环在编译时完全展开为具体的硬件描述
- **参数化设计**：支持使用参数控制生成的硬件规模和结构
- **层次化生成**：支持嵌套For循环生成复杂的二维或多维硬件阵列
- **类型一致性**：生成的所有硬件元素保持类型和接口的一致性

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

### 6.3 使用For语句的并行移位寄存器
```ghdl
module parallel_shift_register:
    parameter(
        WIDTH = 8,
        STAGES = 4
    )
    input(
        wire clk,
        wire rst,
        wire shift_enable,
        wire(WIDTH-1:0) data_in
    )
    output(
        wire(WIDTH-1:0) data_out[STAGES-1:0]
    )
    register(
        # 使用For循环生成多级寄存器
        for i in range(0, STAGES):
            reg(WIDTH-1:0) shift_reg[i]
    )
    
    # 使用For循环生成时序逻辑
    for stage in range(0, STAGES):
        run (clk.posedge):
            if rst:
                shift_reg[stage] = 0
            elsif shift_enable:
                if stage == 0:
                    shift_reg[stage] = data_in
                else:
                    shift_reg[stage] = shift_reg[stage-1]
    
    # 使用For循环连接输出
    for i in range(0, STAGES):
        always:
            data_out[i] = shift_reg[i]
```

### 6.4 使用For语句的存储器模块
```ghdl
module memory_array:
    parameter(
        ADDR_WIDTH = 8,
        DATA_WIDTH = 32,
        DEPTH = 256
    )
    input(
        wire clk,
        wire rst,
        wire write_enable,
        wire(ADDR_WIDTH-1:0) address,
        wire(DATA_WIDTH-1:0) write_data
    )
    output(
        wire(DATA_WIDTH-1:0) read_data
    )
    register(
        # 使用For循环生成存储器阵列
        for i in range(0, DEPTH):
            reg(DATA_WIDTH-1:0) memory[i]
    )
    
    # 写操作
    for addr in range(0, DEPTH):
        run (clk.posedge):
            if rst:
                memory[addr] = 0
            elsif write_enable and (address == addr):
                memory[addr] = write_data
    
    # 读操作 - 组合逻辑
    always:
        read_data = 0
        for addr in range(0, DEPTH):
            if address == addr:
                read_data = memory[addr]
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
6. **生成能力强**：For循环生成语句支持复杂硬件结构的自动生成

## 8. For循环生成语句的应用场景

### 8.1 典型应用
- **存储器阵列**：生成大规模的存储器单元阵列
- **并行处理器**：生成多个相同的处理单元
- **流水线设计**：生成多级流水线寄存器
- **总线接口**：生成多位宽的总线连接逻辑
- **数组操作**：生成并行的数组处理逻辑

### 8.2 设计优势
- **代码复用**：避免重复编写相似的硬件描述
- **参数化**：通过参数控制生成的硬件规模
- **可维护性**：修改一处代码即可影响所有生成的实例
- **可扩展性**：轻松调整硬件规模而无需重写代码
- **错误减少**：自动生成减少手工编写的错误

### 8.3 注意事项
- For循环在编译时完全展开，不是运行时循环
- 循环变量必须是编译时常量或参数
- 生成的硬件结构在物理上是并行存在的
- 需要考虑生成硬件的资源消耗和时序约束