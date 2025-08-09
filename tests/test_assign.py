#!/usr/bin/env python3
"""
测试assign功能的解析
"""

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gracehdl_compiler import GraceHDLCompiler

def test_assign_parsing():
    """测试assign功能的解析"""
    
    # 创建一个简单的测试文件
    test_content = """module test_assign:
        input(
            wire a,
            wire b
        )
        
        output(
            wire y
        )
        
        assign:
        y = a & b
"""
    
    # 写入测试文件
    test_file = "test_assign.ghdl"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    try:
        print("测试assign功能解析...")
        
        # 创建编译器实例
        compiler = GraceHDLCompiler()
        
        # 编译文件
        result = compiler.compile_file(test_file, verbose=True)
        
        if result:
            print("✓ assign功能解析成功！")
            print("生成的Verilog代码:")
            print("-" * 40)
            with open(test_file.replace('.ghdl', '.v'), 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            print("✗ assign功能解析失败")
            
    except Exception as e:
        print(f"✗ 编译过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)
        verilog_file = test_file.replace('.ghdl', '.v')
        if os.path.exists(verilog_file):
            os.remove(verilog_file)

if __name__ == "__main__":
    test_assign_parsing()