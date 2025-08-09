# GraceHDL 追平 Verilog 功能开发计划

## 📋 项目概述

本文档详细规划了 GraceHDL 追平 Verilog 核心功能的开发计划。目标是在保持 GraceHDL 简洁语法优势的同时，实现与 Verilog 功能对等的硬件描述能力。

## 🎯 开发目标

- **功能完整性**: 覆盖 Verilog 90% 的常用功能
- **语法一致性**: 保持 GraceHDL 的 Python 风格语法
- **教学友好性**: 优化学习曲线和使用体验
- **工业可用性**: 支持实际项目开发需求

## 📊 当前功能状态评估

### ✅ 已完成功能 (70% 完成度)
1. **基础语法支持**
   - ✅ 模块定义、端口声明、寄存器定义
   - ✅ 时序逻辑 (`run`) 和组合逻辑 (`always`)
   - ✅ 控制结构 (`if-else`, `case`)
   - ✅ 数据类型 (`wire`, `reg`) 和位宽支持

2. **高级语法特性**
   - ✅ 数组支持 (声明、索引访问、赋值)
   - ✅ 模块实例化 (按名称端口连接)
   - ✅ 注释系统 (单行、多行、行内注释)
   - ✅ For循环生成语句 (编译时展开)
   - ✅ 新数值格式 `(value, base, width)`

3. **编译器基础设施**
   - ✅ 完整的词法分析器
   - ✅ 健壮的语法分析器
   - ✅ 标准Verilog代码生成器
   - ✅ 错误处理机制

## 🚀 需要开发的核心功能

### 第一优先级：立即开发 (2-3周)

#### 1. 参数化模块系统 ⭐⭐⭐⭐⭐
**重要性**: Verilog parameter 功能的等价实现
**开发时间**: 1周
**技术难度**: 中等

**目标语法**:
```ghdl
module counter:
    parameter(
        WIDTH = 8,
        MAX_COUNT = 255,
        RESET_VALUE = 0
    )
    input(
        wire clk,
        wire reset
    )
    output(
        wire(WIDTH-1:0) count
    )
    
    register(
        reg(WIDTH-1:0) counter_reg
    )
    
    run(posedge clk):
        if reset:
            counter_reg = (RESET_VALUE, d, WIDTH)
        elif counter_reg == MAX_COUNT:
            counter_reg = (RESET_VALUE, d, WIDTH)
        else:
            counter_reg = counter_reg + (1, d, WIDTH)
    
    always:
        count = counter_reg

# 实例化时传递参数
counter_8bit: counter(WIDTH=8, MAX_COUNT=255)
counter_16bit: counter(WIDTH=16, MAX_COUNT=65535)
```

**实现要点**:
- 扩展词法分析器: 添加 `parameter` 关键字
- 修改语法分析器: 支持参数块语法解析
- 创建 AST 节点: `ParameterSection`, `ParameterDeclaration`
- 实现参数替换: 编译时参数值替换机制
- 更新代码生成器: 输出 Verilog parameter 声明
- 支持参数表达式: 参数间的算术运算

#### 2. 枚举类型系统 ⭐⭐⭐⭐⭐
**重要性**: 状态机设计的核心需求
**开发时间**: 1周
**技术难度**: 中等

**目标语法**:
```ghdl
module state_machine:
    enum State:
        IDLE = 0,
        FETCH = 1,
        DECODE = 2,
        EXECUTE = 3,
        WRITEBACK = 4
    
    enum Operation:
        ADD = (0, b, 3),
        SUB = (1, b, 3),
        MUL = (2, b, 3),
        DIV = (3, b, 3)
    
    input(
        wire clk,
        wire reset,
        wire(2:0) op_code
    )
    output(
        wire(2:0) current_state,
        wire(2:0) current_op
    )
    
    register(
        State state_reg,
        Operation op_reg
    )
    
    run(posedge clk):
        if reset:
            state_reg = State.IDLE
            op_reg = Operation.ADD
        else:
            case state_reg:
                State.IDLE: 
                    state_reg = State.FETCH
                    op_reg = Operation(op_code)
                State.FETCH: state_reg = State.DECODE
                State.DECODE: state_reg = State.EXECUTE
                State.EXECUTE: state_reg = State.WRITEBACK
                State.WRITEBACK: state_reg = State.IDLE
    
    always:
        current_state = state_reg
        current_op = op_reg
```

**实现要点**:
- 扩展词法分析器: 添加 `enum` 关键字
- 修改语法分析器: 支持枚举定义语法
- 创建 AST 节点: `EnumDefinition`, `EnumValue`
- 实现类型检查: 枚举类型的赋值和比较验证
- 更新代码生成器: 输出 Verilog localparam 定义
- 支持枚举转换: 数值到枚举、枚举到数值的转换

#### 3. 连续赋值语句 ⭐⭐⭐⭐
**重要性**: Verilog assign 语句的等价实现
**开发时间**: 1周
**技术难度**: 简单

**目标语法**:
```ghdl
module logic_gates:
    input(
        wire a,
        wire b,
        wire c,
        wire(7:0) data_in
    )
    output(
        wire y1,
        wire y2,
        wire(7:0) data_out,
        wire parity
    )
    
    # 连续赋值块
    assign:
        y1 = a & b
        y2 = a | (b ^ c)
        data_out = data_in
        parity = ^data_in  # XOR reduction
        
    # 也可以在 always 块中使用
    always:
        # 组合逻辑
        result = a ? b : c
```

**实现要点**:
- 扩展词法分析器: 添加 `assign` 关键字
- 修改语法分析器: 支持连续赋值块语法
- 创建 AST 节点: `AssignSection`, `ContinuousAssignment`
- 更新代码生成器: 输出 Verilog assign 语句
- 支持归约运算符: `&`, `|`, `^`, `~&`, `~|`, `~^`

### 第二优先级：核心增强 (3-4周)

#### 4. 函数定义系统 ⭐⭐⭐⭐
**重要性**: 代码复用和模块化设计
**开发时间**: 1周
**技术难度**: 中等

**目标语法**:
```ghdl
module alu:
    input(wire(7:0) a, wire(7:0) b, wire(1:0) op)
    output(wire(8:0) result, wire parity_out)
    
    # 简单函数定义 - 类似Python
    def add(x, y):
        return x + y
    
    def parity(data):
        return ^data  # XOR归约
    
    def select(condition, true_val, false_val):
        return true_val if condition else false_val
    
    always:
        # 直接调用函数，像Python一样简单
        if op == 0:
            result = add(a, b)
        elif op == 1:
            result = a - b
        elif op == 2:
            result = a * b
        else:
            result = 0
            
        parity_out = parity(a)
```

**实现要点**:
- 扩展词法分析器: 添加 `def`, `return` 关键字
- 修改语法分析器: 支持Python风格函数定义
- 创建 AST 节点: `FunctionDef`, `FunctionCall`, `ReturnStatement`
- 实现类型推断: 自动推断函数参数和返回值类型
- 更新代码生成器: 输出 Verilog function 定义

#### 5. 高级数组和存储器 ⭐⭐⭐⭐
**重要性**: 复杂存储器设计支持
**开发时间**: 1周
**技术难度**: 中等

**目标语法**:
```ghdl
module memory:
    input(wire clk, wire(9:0) addr, wire(31:0) data_in, wire write_en)
    output(wire(31:0) data_out)
    
    # 简单的数组声明 - 像Python列表
    memory = [0] * 1024        # 1K个32位存储单元
    cache = [[0] * 4] * 16     # 16行，每行4路的缓存
    buffer = [0, 0, 0, 0]      # 固定大小缓冲区
    
    run(posedge clk):
        if write_en:
            memory[addr] = data_in
    
    always:
        data_out = memory[addr]
```

**实现要点**:
- 扩展数组语法: 支持Python风格的列表声明 `[0] * size`
- 实现多维数组: 支持 `[[0] * cols] * rows` 语法
- 简化数组访问: 直接使用 `array[index]` 语法
- 更新代码生成器: 转换为标准 Verilog 数组语法

#### 6. 位选择和拼接操作 ⭐⭐⭐⭐
**重要性**: 位操作是硬件设计基础
**开发时间**: 1周
**技术难度**: 中等

**目标语法**:
```ghdl
module bit_ops:
    input(
        wire(15:0) data, 
        wire(7:0) a, 
        wire(7:0) b
    )
    output(wire(7:0) high, 
    wire(7:0) low, 
    wire(15:0) joined
    )
    
    always:
        # 位选择 - 像Python切片一样简单
        high = data[15:8]      # 高8位
        low = data[7:0]        # 低8位
        bit7 = data[7]         # 单个位
        
        # 位拼接 - 用+号连接
        joined = a + b         # 拼接两个字节
        
        # 位重复 - 用*号重复
        repeated = a * 4       # 重复4次
```

**实现要点**:
- 扩展语法分析器: 支持Python风格切片 `signal[high:low]`
- 实现位拼接: 重载 `+` 运算符用于位拼接
- 支持位重复: 重载 `*` 运算符用于位重复
- 更新代码生成器: 转换为标准 Verilog 位操作语法

### 第三优先级：实用性提升 (4-5周)

#### 7. 接口定义系统 ⭐⭐⭐
**重要性**: 标准化接口设计
**开发时间**: 1周
**技术难度**: 中等

**目标语法**:
```ghdl
interface AXI4_Lite:
    parameter(
        ADDR_WIDTH = 32,
        DATA_WIDTH = 32
    )
    
    # 写地址通道
    input(
        wire(ADDR_WIDTH-1 to 0) awaddr,
        wire awvalid
    )
    output(
        wire awready
    )
    
    # 写数据通道
    input(
        wire(DATA_WIDTH-1 to 0) wdata,
        wire((DATA_WIDTH/8)-1 to 0) wstrb,
        wire wvalid
    )
    output(
        wire wready
    )
    
    # 写响应通道
    input(
        wire bready
    )
    output(
        wire(1 to 0) bresp,
        wire bvalid
    )

module axi_slave:
    port axi: AXI4_Lite(ADDR_WIDTH=32, DATA_WIDTH=32)
    
    register(
        reg(31 to 0) registers[255 to 0]
    )
    
    always:
        axi.awready = 1
        axi.wready = 1
        axi.bresp = 0b00  # OKAY response
```

#### 8. 生成块扩展 ⭐⭐⭐
**重要性**: 参数化硬件生成
**开发时间**: 1周
**技术难度**: 中等

**目标语法**:
```ghdl
module parallel_processor:
    parameter(
        NUM_CORES = 4,
        DATA_WIDTH = 32
    )
    
    input(
        wire clk,
        wire reset,
        wire(DATA_WIDTH-1 to 0) data_in[NUM_CORES-1 to 0]
    )
    output(
        wire(DATA_WIDTH-1 to 0) data_out[NUM_CORES-1 to 0]
    )
    
    # 生成块
    generate:
        for i in range(NUM_CORES):
            # 为每个核心生成处理单元
            processing_unit core_inst:
                .clk(clk)
                .reset(reset)
                .data_in(data_in[i])
                .data_out(data_out[i])
                .core_id(i)
        
        # 条件生成
        if NUM_CORES > 2:
            # 生成额外的仲裁逻辑
            arbiter arb_inst:
                .clk(clk)
                .reset(reset)
```

#### 9. 多时钟域支持 ⭐⭐⭐
**重要性**: 实际设计中的常见需求
**开发时间**: 1周
**技术难度**: 中等

**目标语法**:
```ghdl
module clock_domain_crossing:
    input(
        wire clk_a,
        wire clk_b,
        wire reset_a,
        wire reset_b,
        wire(7 to 0) data_in
    )
    output(
        wire(7 to 0) data_out,
        wire data_valid
    )
    
    register(
        reg(7 to 0) data_reg clocked_by clk_a,
        reg(7 to 0) sync_reg1 clocked_by clk_b,
        reg(7 to 0) sync_reg2 clocked_by clk_b,
        reg valid_reg clocked_by clk_b
    )
    
    run(clk_a.posedge):
        if reset_a:
            data_reg = 0
        else:
            data_reg = data_in
    
    run(clk_b.posedge):
        if reset_b:
            sync_reg1 = 0
            sync_reg2 = 0
            valid_reg = 0
        else:
            sync_reg1 = data_reg
            sync_reg2 = sync_reg1
            valid_reg = 1
    
    always:
        data_out = sync_reg2
        data_valid = valid_reg
```

### 第四优先级：验证和调试 (5-6周)

#### 10. 断言系统 ⭐⭐
**重要性**: 设计验证
**开发时间**: 1周
**技术难度**: 简单

**目标语法**:
```ghdl
module counter_with_assertions:
    parameter(
        WIDTH = 8,
        MAX_COUNT = 255
    )
    
    input(
        wire clk,
        wire reset
    )
    output(
        wire(WIDTH-1 to 0) count
    )
    
    register(
        reg(WIDTH-1 to 0) counter_reg
    )
    
    run(clk.posedge):
        if reset:
            counter_reg = 0
        else:
            counter_reg = counter_reg + 1
    
    always:
        count = counter_reg
        
        # 功能断言
        assert(counter_reg <= MAX_COUNT, "Counter overflow detected")
        
        # 时序断言
        assert(reset implies (count == 0), "Reset assertion failed")
        
        # 覆盖率断言
        cover(counter_reg == MAX_COUNT, "Maximum count reached")
```

#### 11. 测试台自动生成 ⭐⭐
**重要性**: 教学和验证便利性
**开发时间**: 1周
**技术难度**: 中等

**目标语法**:
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
    signal count: wire(7 to 0)
    
    # 被测模块实例化
    dut: counter(WIDTH=8, MAX_COUNT=255)
        .clk(clk)
        .reset(reset)
        .count(count)
    
    # 测试序列
    test_sequence:
        # 复位测试
        reset = 1
        wait for 2 * CLK_PERIOD
        assert(count == 0, "Reset test failed")
        
        # 正常计数测试
        reset = 0
        wait for TEST_CYCLES * CLK_PERIOD
        assert(count == TEST_CYCLES, "Count test failed")
        
        # 溢出测试
        wait for 200 * CLK_PERIOD
        assert(count == 0, "Overflow test failed")
    
    # 波形输出
    dump_waves to "counter_test.vcd"
    
    # 测试报告
    report_coverage
```

## 📅 开发时间表

### 第1阶段 (第1-3周): 核心功能
- **Week 1**: 参数化模块系统
  - 词法分析器扩展
  - 语法分析器修改
  - AST节点实现
  - 基础测试用例
  
- **Week 2**: 枚举类型系统
  - 枚举定义语法
  - 类型检查机制
  - 代码生成优化
  - 状态机测试用例
  
- **Week 3**: 连续赋值语句
  - assign块语法
  - 归约运算符支持
  - 代码生成实现
  - 组合逻辑测试

### 第2阶段 (第4-6周): 增强功能
- **Week 4**: 函数定义系统
- **Week 5**: 高级数组操作
- **Week 6**: 位选择和拼接

### 第3阶段 (第7-9周): 高级特性
- **Week 7**: 接口定义系统
- **Week 8**: 生成块扩展
- **Week 9**: 多时钟域支持

### 第4阶段 (第10-12周): 验证工具
- **Week 10**: 断言系统
- **Week 11**: 测试台生成
- **Week 12**: 集成测试和优化

## 🎯 成功标准

### 功能完整性
- [ ] 支持所有 Verilog 常用语法结构
- [ ] 生成标准兼容的 Verilog 代码
- [ ] 通过完整的测试套件验证

### 性能指标
- [ ] 编译速度: < 1秒 (中等规模设计)
- [ ] 内存使用: < 100MB (大型设计)
- [ ] 错误检测: 90% 语法错误捕获率

### 用户体验
- [ ] 清晰的错误信息
- [ ] 完整的文档和示例
- [ ] 良好的IDE集成支持

## 📝 下一步行动

1. **确认语法规范**: 等待用户提供详细的GraceHDL语法规范
2. **制定实施计划**: 根据语法规范调整开发优先级
3. **开始第一阶段开发**: 从参数化模块系统开始实施
4. **建立测试框架**: 为每个新功能创建测试用例
5. **持续集成**: 确保新功能不破坏现有功能

---

**准备就绪，等待您的语法规范总结！** 🚀