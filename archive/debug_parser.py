#!/usr/bin/env python3
"""
调试语法分析器
"""

from src.parser import GraceHDLParser

def debug_parser():
    parser = GraceHDLParser()
    parser.build(debug=True)
    
    test_code = """module test
input wire a
output wire y
assign y = a
"""
    
    print("测试代码:")
    print(repr(test_code))
    print("\n开始语法分析...")
    
    try:
        result = parser.parser.parse(test_code, lexer=parser.lexer, debug=True)
        print("解析成功！")
        print(f"结果: {result}")
    except Exception as e:
        print(f"解析失败: {e}")

if __name__ == "__main__":
    debug_parser()