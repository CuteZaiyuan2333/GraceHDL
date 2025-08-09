#!/usr/bin/env python3
"""
完整的assign功能测试
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from gracehdl_compiler import GraceHDLCompiler

def test_assign_functionality():
    """测试assign功能的完整实现"""
    
    print("=== GraceHDL assign功能完整测试 ===\n")
    
    # 测试用例1: 简单的逻辑门
    test_cases = [
        {
            "name": "简单AND门",
            "content": """module and_gate:
    input(
        wire a,
        wire b
    )
    
    output(
        wire y
    )
    
    assign:
        y = a & b
""",
            "expected": "assign y = (a & b);"
        },
        {
            "name": "多个assign语句",
            "content": """module multi_assign:
    input(
        wire a,
        wire b,
        wire c
    )
    
    output(
        wire x,
        wire y,
        wire z
    )
    
    assign:
        x = a & b
        y = a | b
        z = a ^ b
""",
            "expected": ["assign x = (a & b);", "assign y = (a | b);", "assign z = (a ^ b);"]
        },
        {
            "name": "复杂表达式",
            "content": """module complex_assign:
    input(
        wire a,
        wire b,
        wire c,
        wire d
    )
    
    output(
        wire result
    )
    
    assign:
        result = (a & b) | (c & d)
""",
            "expected": "assign result = ((a & b) | (c & d));"
        }
    ]
    
    compiler = GraceHDLCompiler()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"测试用例 {i}: {test_case['name']}")
        print("-" * 40)
        
        # 创建测试文件
        test_file = f"test_case_{i}.ghdl"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_case['content'])
        
        try:
            # 编译
            print(f"编译 {test_file}...")
            success = compiler.compile_file(test_file)
            
            if success:
                print("✓ 编译成功")
                
                # 读取生成的Verilog文件
                output_file = test_file.replace('.ghdl', '.v')
                if os.path.exists(output_file):
                    with open(output_file, 'r', encoding='utf-8') as f:
                        verilog_code = f.read()
                    
                    print("生成的Verilog代码:")
                    print(verilog_code)
                    
                    # 检查是否包含期望的assign语句
                    expected = test_case['expected']
                    if isinstance(expected, str):
                        expected = [expected]
                    
                    all_found = True
                    for exp in expected:
                        if exp not in verilog_code:
                            print(f"✗ 未找到期望的语句: {exp}")
                            all_found = False
                    
                    if all_found:
                        print("✓ 所有期望的assign语句都已生成")
                    
                    # 清理生成的文件
                    os.remove(output_file)
                else:
                    print("✗ 未找到生成的Verilog文件")
                
            else:
                print("✗ 编译失败")
                
        except Exception as e:
            print(f"✗ 编译出错: {e}")
        
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)
        
        print("\n")
    
    print("=== assign功能测试完成 ===")

if __name__ == "__main__":
    test_assign_functionality()