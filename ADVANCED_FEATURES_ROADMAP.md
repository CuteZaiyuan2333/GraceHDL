# GraceHDL 高级功能开发路线图

## 📊 当前功能状态评估

### ✅ 已完成的核心功能 (90%完成度)
1. **基础语法支持**
   - 模块定义、端口声明、寄存器定义
   - 时序逻辑 (`run`) 和组合逻辑 (`always`)
   - 控制结构 (`if-else`, `case`)
   - 数据类型 (`wire`, `reg`) 和位宽支持

2. **高级语法特性**
   - 数组支持 (声明、索引访问、赋值)
   - 模块实例化 (按名称端口连接)
   - 注释系统 (单行、多行、行内注释)
   - 新数值格式 `(value, base, width)`

3. **编译器基础设施**
   - 完整的词法分析器
   - 健壮的语法分析器
   - 标准Verilog代码生成器
   - 错误处理机制

## 🚀 需要开发的高级功能

### 第一优先级：核心增强功能 (2-3周)

#### 1. 参数化模块系统 🎯
**重要性**: ⭐⭐⭐⭐⭐ (教学和实用性必需)
```ghdl
module counter:
    parameter(
        WIDTH = 8,
        MAX_COUNT = 255
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
            counter_reg = (0, d, WIDTH)
        elif counter_reg == MAX_COUNT:
            counter_reg = (0, d, WIDTH)
        else:
            counter_reg = counter_reg + (1, d, WIDTH)
    
    always:
        count = counter_reg
```

**实现要点**:
- 扩展语法分析器支持 `parameter()` 块
- 实现参数传递和替换机制
- 支持参数表达式计算
- 生成参数化的Verilog代码

#### 2. For循环生成语句 🔄
**重要性**: ⭐⭐⭐⭐ (简化重复逻辑设计)
```ghdl
module parallel_adder:
    input(
        wire(7:0) a,
        wire(7:0) b
    )
    output(
        wire(7:0) sum,
        wire cout
    )
    
    register(
        reg(7:0) carry
    )
    
    always:
        carry[0] = 0
        for i in range(8):
            sum[i] = a[i] ^ b[i] ^ carry[i]
            carry[i+1] = (a[i] & b[i]) | (a[i] & carry[i]) | (b[i] & carry[i])
        cout = carry[8]
```

**实现要点**:
- 添加 `for` 循环语法支持
- 实现循环展开机制
- 支持 `range()` 函数
- 生成展开后的Verilog代码

#### 3. 枚举类型系统 📝
**重要性**: ⭐⭐⭐⭐ (状态机设计必需)
```ghdl
module state_machine:
    enum State:
        IDLE = 0,
        FETCH = 1,
        DECODE = 2,
        EXECUTE = 3,
        WRITEBACK = 4
    
    input(
        wire clk,
        wire reset
    )
    output(
        wire(2:0) current_state
    )
    
    register(
        State state_reg
    )
    
    run(posedge clk):
        if reset:
            state_reg = State.IDLE
        else:
            case state_reg:
                State.IDLE: state_reg = State.FETCH
                State.FETCH: state_reg = State.DECODE
                State.DECODE: state_reg = State.EXECUTE
                State.EXECUTE: state_reg = State.WRITEBACK
                State.WRITEBACK: state_reg = State.IDLE
    
    always:
        current_state = state_reg
```

**实现要点**:
- 添加 `enum` 类型定义语法
- 实现枚举值到数值的映射
- 支持枚举类型的比较和赋值
- 生成对应的Verilog参数定义

### 第二优先级：实用性增强 (3-4周)

#### 4. 函数定义系统 🔧
**重要性**: ⭐⭐⭐ (代码复用和模块化)
```ghdl
module alu:
    function add(a: wire(7:0), b: wire(7:0)) -> wire(8:0):
        return a + b
    
    function multiply(a: wire(3:0), b: wire(3:0)) -> wire(7:0):
        return a * b
    
    input(
        wire(7:0) operand_a,
        wire(7:0) operand_b,
        wire(1:0) operation
    )
    output(
        wire(8:0) result
    )
    
    always:
        case operation:
            (0, d, 2): result = add(operand_a, operand_b)
            (1, d, 2): result = operand_a - operand_b
            (2, d, 2): result = multiply(operand_a[3:0], operand_b[3:0])
            default: result = (0, d, 9)
```

#### 5. 高级数组操作 📊
**重要性**: ⭐⭐⭐ (存储器和缓存设计)
```ghdl
module memory_controller:
    input(
        wire clk,
        wire(7:0) address,
        wire(7:0) write_data,
        wire write_enable,
        wire read_enable
    )
    output(
        wire(7:0) read_data
    )
    
    register(
        reg(7:0) memory[255:0]
    )
    
    run(posedge clk):
        if write_enable:
            memory[address] = write_data
    
    always:
        if read_enable:
            read_data = memory[address]
        else:
            read_data = (0, d, 8)
```

#### 6. 接口定义系统 🔌
**重要性**: ⭐⭐⭐ (标准化设计)
```ghdl
interface AXI4_Lite:
    input(
        wire(31:0) awaddr,
        wire awvalid,
        wire(31:0) wdata,
        wire(3:0) wstrb,
        wire wvalid,
        wire bready,
        wire(31:0) araddr,
        wire arvalid,
        wire rready
    )
    output(
        wire awready,
        wire wready,
        wire(1:0) bresp,
        wire bvalid,
        wire arready,
        wire(31:0) rdata,
        wire(1:0) rresp,
        wire rvalid
    )

module axi_slave:
    port axi: AXI4_Lite
    
    # 使用接口信号
    always:
        axi.awready = 1
        axi.wready = 1
```

### 第三优先级：验证和调试支持 (4-5周)

#### 7. 断言系统 ✅
**重要性**: ⭐⭐ (验证和调试)
```ghdl
module counter_with_assertions:
    input(
        wire clk,
        wire reset
    )
    output(
        wire(7:0) count
    )
    
    register(
        reg(7:0) counter_reg
    )
    
    run(posedge clk):
        if reset:
            counter_reg = (0, d, 8)
        else:
            counter_reg = counter_reg + (1, d, 8)
    
    always:
        count = counter_reg
        
        # 断言：计数器不应该溢出
        assert(counter_reg <= (255, d, 8), "Counter overflow detected")
        
        # 断言：复位后计数器应该为0
        assert(reset -> (count == (0, d, 8)), "Reset assertion failed")
```

#### 8. 测试台自动生成 🧪
**重要性**: ⭐⭐ (教学和验证)
```ghdl
testbench for counter:
    # 自动生成时钟
    clock clk period 10ns
    
    # 测试序列
    test_sequence:
        reset = 1
        wait 20ns
        reset = 0
        wait 100ns
        assert(count == (10, d, 8))
        
    # 波形输出
    dump_waves "counter_test.vcd"
```

### 第四优先级：高级特性 (5-6周)

#### 9. 多时钟域支持 ⏰
**重要性**: ⭐⭐ (实际设计需要)
```ghdl
module clock_domain_crossing:
    input(
        wire clk_a,
        wire clk_b,
        wire(7:0) data_in
    )
    output(
        wire(7:0) data_out
    )
    
    register(
        reg(7:0) sync_reg1 @ clk_b,
        reg(7:0) sync_reg2 @ clk_b,
        reg(7:0) data_reg @ clk_a
    )
    
    run(posedge clk_a):
        data_reg = data_in
    
    run(posedge clk_b):
        sync_reg1 = data_reg
        sync_reg2 = sync_reg1
    
    always:
        data_out = sync_reg2
```

#### 10. 生成块 (Generate) 🏗️
**重要性**: ⭐⭐ (参数化设计)
```ghdl
module parallel_multiplier:
    parameter(
        WIDTH = 8
    )
    
    input(
        wire(WIDTH-1:0) a,
        wire(WIDTH-1:0) b
    )
    output(
        wire(2*WIDTH-1:0) product
    )
    
    generate:
        for i in range(WIDTH):
            for j in range(WIDTH):
                wire partial_product = a[i] & b[j]
                # 加法器树逻辑
```

## 🎯 开发优先级和时间安排

### 第1阶段 (2-3周): 核心增强
1. **参数化模块** (1周)
2. **For循环生成** (1周)  
3. **枚举类型** (1周)

### 第2阶段 (3-4周): 实用性提升
4. **函数定义** (1周)
5. **高级数组操作** (1周)
6. **接口定义** (1周)

### 第3阶段 (4-5周): 验证支持
7. **断言系统** (1周)
8. **测试台生成** (1周)

### 第4阶段 (5-6周): 高级特性
9. **多时钟域** (1周)
10. **生成块** (1周)

## 📋 实现策略

### 技术架构
1. **词法分析器扩展**: 添加新关键字和操作符
2. **语法分析器增强**: 扩展语法规则
3. **AST节点扩展**: 新增节点类型
4. **代码生成器优化**: 支持新特性的Verilog生成

### 测试策略
1. **单元测试**: 每个新功能都有对应测试用例
2. **集成测试**: 复杂设计的端到端测试
3. **回归测试**: 确保新功能不破坏现有功能

### 文档更新
1. **语法规范更新**: 详细的语法说明
2. **用户指南更新**: 使用示例和最佳实践
3. **开发者文档**: 内部实现说明

## 🎓 教学价值评估

### 高教学价值功能
1. **参数化模块** - 可重用设计概念
2. **枚举类型** - 状态机设计
3. **For循环** - 规律性设计
4. **函数定义** - 模块化编程

### 中等教学价值功能
1. **接口定义** - 标准化设计
2. **断言系统** - 验证概念
3. **测试台生成** - 测试方法

### 专业级功能
1. **多时钟域** - 高级时序设计
2. **生成块** - 高级参数化

## 🚀 开始实施

建议从**参数化模块**开始实施，因为：
1. 教学价值最高
2. 实现相对简单
3. 为后续功能奠定基础
4. 学生和教师需求最迫切

下一步行动：
1. 设计参数化模块的语法规则
2. 扩展词法分析器和语法分析器
3. 实现AST节点和代码生成
4. 创建测试用例验证功能