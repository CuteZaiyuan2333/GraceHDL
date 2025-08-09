#!/usr/bin/env python3
"""
测试编译器
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.lexer import GraceHDLLexer
from src.parser import GraceHDLParser
from src.verilog_generator import VerilogGenerator

def test_compiler():
    # 创建编译器组件
    lexer = GraceHDLLexer()
    lexer.build()
    
    parser = GraceHDLParser()
    parser.build()
    
    generator = VerilogGenerator()
    
    # 测试代码
    test_code = """module test
input wire a
output wire y
assign y = a
"""
    
    print("测试代码:")
    print(test_code)
    print("\n开始编译...")
    
    try:
        # 设置词法分析器输入
        lexer.input(test_code)
        
        # 语法分析
        ast = parser.parser.parse(test_code, lexer=lexer)
        
        if ast is None:
            print("语法分析失败")
            return False
        
        print("语法分析成功！")
        print(f"AST: {ast}")
        
        # 代码生成
        verilog_code = generator.generate(ast)
        
        print("\n生成的Verilog代码:")
        print(verilog_code)
        
        # 写入文件
        with open('test_output.v', 'w', encoding='utf-8') as f:
            f.write(verilog_code)
        
        print("\n编译成功！输出文件: test_output.v")
        return True
        
    except Exception as e:
        print(f"编译失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_compiler()