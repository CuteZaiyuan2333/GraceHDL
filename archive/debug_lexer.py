#!/usr/bin/env python3
"""
调试词法分析器
"""

from src.lexer import GraceHDLLexer

def debug_lexer():
    lexer = GraceHDLLexer()
    lexer.build()
    
    with open('test_simple.ghdl', 'r', encoding='utf-8') as f:
        code = f.read()
    
    print("输入代码:")
    print(repr(code))
    print("\n词法分析结果:")
    
    lexer.lexer.input(code)
    
    while True:
        tok = lexer.token()  # 使用我们的自定义token方法
        if not tok:
            break
        print(f"Token: {tok.type:15} Value: {repr(tok.value):15} Line: {tok.lineno}")

if __name__ == "__main__":
    debug_lexer()