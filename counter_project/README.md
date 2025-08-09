# 计数器项目 (Counter Project)

这个项目展示了使用 GraceHDL 设计的几个实用数字电路，并成功编译为标准的 Verilog HDL 代码。

## 项目文件

### 1. advanced_counter.ghdl / advanced_counter.v
**高级8位计数器**
- **功能**: 带有使能控制和上下计数功能的8位计数器
- **输入**: 
  - `clk`: 时钟信号
  - `reset`: 复位信号
  - `enable`: 使能信号
  - `up_down`: 计数方向控制（1=向上，0=向下）
- **输出**:
  - `count[7:0]`: 8位计数值
  - `overflow`: 上溢标志
  - `underflow`: 下溢标志
- **特性**: 
  - 同步复位
  - 可控制计数方向
  - 溢出检测

### 2. pwm_counter.ghdl / pwm_counter.v
**PWM计数器**
- **功能**: 生成PWM信号的计数器
- **输入**:
  - `clk`: 时钟信号
  - `reset`: 复位信号
  - `enable`: 使能信号
- **输出**:
  - `count[7:0]`: 当前计数值
  - `pwm_out`: PWM输出信号
  - `period_complete`: 周期完成标志
- **特性**:
  - 固定50%占空比（duty_cycle = 128）
  - 8位分辨率PWM输出

### 3. traffic_light.ghdl / traffic_light.v
**交通灯状态机**
- **功能**: 简单的三状态交通灯控制器
- **输入**:
  - `clk`: 时钟信号
  - `reset`: 复位信号
  - `sensor`: 传感器输入（预留）
- **输出**:
  - `red`: 红灯控制
  - `yellow`: 黄灯控制
  - `green`: 绿灯控制
  - `state[1:0]`: 当前状态
- **状态**:
  - 状态0: 红灯
  - 状态1: 黄灯
  - 状态2: 绿灯
- **特性**:
  - 自动状态转换
  - 可配置定时器

## GraceHDL 新特性展示

这些设计展示了 GraceHDL 的以下新特性：

1. **新数值格式**: `(value, base, width)`
   - `(0, d, 8)` → `8'd0` (8位十进制)
   - `(255, d, 8)` → `8'd255` (8位十进制)
   - `(1, b, 1)` → `1'b1` (1位二进制)

2. **简洁的模块定义语法**:
   ```ghdl
   module name:
       input(...)
       output(...)
       register(...)
   ```

3. **清晰的时序和组合逻辑分离**:
   - `run (clk.posedge):` 用于时序逻辑
   - `always:` 用于组合逻辑

## 编译结果

所有 GraceHDL 文件都成功编译为标准的 Verilog HDL 代码，生成的代码：
- 语法正确，符合 Verilog 标准
- 结构清晰，易于理解
- 可以直接用于 FPGA 或 ASIC 设计流程

### 4. simple_test.ghdl / simple_test.v
**简单计数器测试**
- **功能**: 基础的8位计数器实现
- **特性**: 演示基本的 GraceHDL 语法结构

### 5. state_machine_test.ghdl
**Case语句测试**
- **功能**: 演示 case 语句的使用
- **特性**: 简单的状态选择逻辑

## 编译状态

✅ **成功编译的文件**:
- `advanced_counter.ghdl` → `advanced_counter.v`
- `pwm_counter.ghdl` → `pwm_counter.v`  
- `traffic_light.ghdl` → `traffic_light.v`
- `simple_test.ghdl` → `simple_test.v`
- `counter_demo.ghdl` → `counter_demo.v`

🔧 **测试文件**:
- `state_machine_test.ghdl` - Case语句功能验证

## 使用方法

使用命令行编译器：
```bash
python gracehdl_compiler.py <input.ghdl> [-o output.v]
```

例如：
```bash
python gracehdl_compiler.py counter_project\advanced_counter.ghdl -o advanced_counter.v
```

或使用模块接口：
```bash
python -m src.compiler <input.ghdl> <output.v>
```

## 验证结果

所有生成的 Verilog 代码都经过验证：
- 语法正确，符合 IEEE 1364 标准
- 逻辑功能与设计意图一致
- 可以在标准 Verilog 仿真器中运行
- 适用于 FPGA 综合工具