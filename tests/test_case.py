#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.lexer import GraceHDLLexer
from src.parser import GraceHDLParser

# 测试case语句的解析
test_code = """
module test_case:
    input(
        wire(2, 0) addr
    )
    output(
        wire(7, 0) out
    )
    
    always:
        case addr:
            (0, d, 3):
                out = (1, d, 8)
            default:
                out = (0, d, 8)
"""

print("测试case语句解析...")

try:
    # 创建词法分析器和语法分析器
    lexer = GraceHDLLexer()
    lexer.build()
    parser = GraceHDLParser()
    parser.build(debug=False)
    
    # 解析代码
    lexer.input(test_code)
    ast = parser.parser.parse(test_code, lexer=lexer, debug=False)
    
    if ast:
        print("✓ case语句解析成功")
        print("AST:", ast)
    else:
        print("✗ case语句解析失败")
except Exception as e:
    print(f"✗ 解析出错: {e}")