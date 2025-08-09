# GraceHDL 展示文件

本文件夹包含了 GraceHDL 编译器的各种功能展示文件，用于演示 GraceHDL 语言的特性和能力。

## 文件列表

### 1. 基本组合逻辑 (`01_basic_gates.ghdl`)
展示 GraceHDL 的基本组合逻辑设计能力：
- 基本逻辑门（与、或、非、异或）
- 全加器设计
- 多位与门阵列
- 多路选择器
- 译码器设计

**特色功能：**
- 简洁的模块定义语法
- 直观的组合逻辑表达
- 参数化设计支持

### 2. 时序逻辑 (`02_sequential_logic.ghdl`)
展示 GraceHDL 的时序逻辑设计能力：
- D 触发器
- 计数器设计
- 移位寄存器
- 可加载计数器
- 双向移位寄存器
- 分频器

**特色功能：**
- `run` 块时钟驱动语法
- `to` 语句时序赋值
- 清晰的时序逻辑表达

### 3. 状态机 (`03_state_machines.ghdl`)
展示 GraceHDL 的有限状态机设计能力：
- 交通灯控制器
- 序列检测器（1011 序列）
- 自动售货机控制器

**特色功能：**
- 枚举类型定义
- 状态机清晰表达
- 复杂控制逻辑支持

### 4. 参数化模块 (`04_parameterized_modules.ghdl`)
展示 GraceHDL 的参数化设计能力：
- 参数化计数器
- 参数化移位寄存器
- 参数化 FIFO
- 参数化 ALU
- 参数化存储器

**特色功能：**
- 灵活的参数定义
- 可重用的模块设计
- 泛型编程支持

### 5. 测试台展示 (`05_testbench_demo.ghdl`)
展示 GraceHDL 的自动测试台生成功能：
- 简单计数器及其测试台
- 简单 ALU 及其测试台
- 简单状态机及其测试台

**特色功能：**
- 自动时钟生成
- 测试序列定义
- 断言验证
- 波形文件输出
- 覆盖率报告

## 编译和运行

### 编译所有展示文件
```bash
python compile_demos.py
```

### 编译单个文件
```bash
python ../src/gracehdl_compiler.py 01_basic_gates.ghdl 01_basic_gates.v
```

## 生成的 Verilog 文件

编译成功后，将生成对应的 Verilog 文件：
- `01_basic_gates.v` - 基本组合逻辑的 Verilog 实现
- `02_sequential_logic.v` - 时序逻辑的 Verilog 实现
- `03_state_machines.v` - 状态机的 Verilog 实现
- `04_parameterized_modules.v` - 参数化模块的 Verilog 实现
- `05_testbench_demo.v` - 测试台的 Verilog 实现

## GraceHDL 语言特色

通过这些展示文件，您可以看到 GraceHDL 语言的以下特色：

1. **简洁的语法**：Python 风格的缩进和语法结构
2. **类型安全**：明确的信号类型和位宽定义
3. **时序清晰**：`run` 块和 `to` 语句的时序逻辑表达
4. **参数化支持**：灵活的参数定义和使用
5. **测试台自动生成**：内置的测试台语法和功能
6. **现代化设计**：面向对象的模块设计理念

## 语法规范

详细的语法规范请参考项目根目录下的 `GraceHDL_语法规范_v2.0.md` 文件。

## 技术支持

如果您在使用过程中遇到问题，请查看：
1. 语法规范文档
2. 编译器错误信息
3. 生成的 Verilog 代码

祝您使用愉快！