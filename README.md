# GraceHDL - 优雅的硬件描述语言

GraceHDL是一种现代化的硬件描述语言，旨在提供简洁、易读的语法来描述数字电路。它采用清晰的模块化语法结构，让硬件设计更加直观和易于理解。

## 特性

- **清晰语法**: 结构化的模块定义，明确分离输入、输出和寄存器声明
- **现代化设计**: 借鉴现代编程语言的优秀特性，支持新式数值格式
- **Verilog兼容**: 编译输出标准Verilog HDL代码，兼容现有工具链
- **时序控制**: 直观的时钟边沿表示法 (`clk.posedge`, `clk.negedge`)
- **控制结构**: 支持 if-else 和 case 语句，适合状态机设计

## 快速开始

### 安装

```bash
pip install -r requirements.txt
```

### 基本用法

1. 编写GraceHDL代码（.ghdl文件）
2. 使用编译器转换为Verilog
3. 使用标准Verilog工具链进行仿真和综合

```bash
python gracehdl_compiler.py input.ghdl -o output.v
```

## 语法示例

### 简单的与门模块

```gracehdl
module and_gate:
    input(wire a, wire b)
    output(wire y)
    
    always:
        y = a & b
```

### 计数器模块

```gracehdl
module counter:
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

### 状态机示例

```gracehdl
module state_machine:
    input(wire clk, wire reset, wire(1:0) input_signal)
    output(reg(1:0) state)
    register(reg(1:0) current_state)
    
    run (clk.posedge):
        if reset:
            current_state = (0, d, 2)
        else:
            case input_signal:
                (0, d, 2):
                    current_state = (1, d, 2)
                (1, d, 2):
                    current_state = (2, d, 2)
                default:
                    current_state = (0, d, 2)
    
    always:
        state = current_state
```

## 文档

- **[GraceHDL 语法标准 v3.0](GraceHDL_语法标准_v3.0.md)** - 完整的语法标准文档（基于实际demo验证）
- **[用户指南](USER_GUIDE.md)** - 详细的使用指南
- **[开发进度](DEVELOPMENT_PROGRESS.md)** - 项目开发状态
- **[高级功能路线图](ADVANCED_FEATURES_ROADMAP.md)** - 未来功能规划
- **[legacy_docs/](legacy_docs/)** - 历史文档归档

## 项目结构

- `src/` - 编译器核心代码
  - `lexer.py` - 词法分析器
  - `parser.py` - 语法分析器  
  - `ast_nodes.py` - AST节点定义
  - `verilog_generator.py` - Verilog代码生成器
  - `compiler.py` - 编译器主接口
- `demos/` - 完整的语法演示示例
- `examples/` - 语言特性示例
- `counter_project/` - 完整项目示例
- `tests/` - 测试文件
- `archive/` - 历史代码归档

## 当前状态

✅ **已实现功能**:
- 基础语法解析 (模块定义、端口声明)
- 时序逻辑 (`run` 块) 和组合逻辑 (`always` 块)
- 控制结构 (if-else, case 语句)
- 新式数值格式 `(value, base, width)`
- Verilog 代码生成

🔧 **开发中功能**:
- 注释支持完善
- 错误报告改进
- 模块实例化
- 数组和存储器支持

详细开发进度请查看 [DEVELOPMENT_PROGRESS.md](DEVELOPMENT_PROGRESS.md)

## 贡献

欢迎提交Issue和Pull Request来改进GraceHDL！