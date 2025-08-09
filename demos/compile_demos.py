#!/usr/bin/env python3
"""
GraceHDL 展示文件编译脚本
编译所有展示文件并生成对应的 Verilog 代码
"""

import os
import sys
import subprocess
from pathlib import Path

# 添加 GraceHDL 根目录路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from gracehdl_compiler import GraceHDLCompiler

def compile_demo_file(input_file, output_file):
    """编译单个展示文件"""
    print(f"正在编译: {input_file}")
    
    try:
        compiler = GraceHDLCompiler()
        success = compiler.compile_file(input_file, output_file)
        
        if success:
            print(f"✓ 编译成功: {output_file}")
            return True
        else:
            print(f"✗ 编译失败: {input_file}")
            return False
            
    except Exception as e:
        print(f"✗ 编译出错: {input_file} - {str(e)}")
        return False

def main():
    """主函数"""
    demos_dir = Path(__file__).parent
    
    # 展示文件列表
    demo_files = [
        "01_basic_gates.ghdl",
        "02_sequential_logic.ghdl", 
        "03_state_machines.ghdl",
        "04_parameterized_modules.ghdl",
        "05_testbench_demo.ghdl"
    ]
    
    print("GraceHDL 展示文件编译器")
    print("=" * 50)
    
    success_count = 0
    total_count = len(demo_files)
    
    for demo_file in demo_files:
        input_path = demos_dir / demo_file
        output_path = demos_dir / (demo_file.replace('.ghdl', '.v'))
        
        if not input_path.exists():
            print(f"✗ 文件不存在: {input_path}")
            continue
            
        if compile_demo_file(str(input_path), str(output_path)):
            success_count += 1
        
        print()
    
    print("=" * 50)
    print(f"编译完成: {success_count}/{total_count} 个文件编译成功")
    
    if success_count == total_count:
        print("🎉 所有展示文件编译成功！")
        return 0
    else:
        print("⚠️  部分文件编译失败，请检查语法错误")
        return 1

if __name__ == "__main__":
    sys.exit(main())