"""
GraceHDL编译器主文件 - 新语法版本
整合词法分析器、语法分析器和代码生成器
"""

import os
import sys
from .lexer import GraceHDLLexer
from .parser import GraceHDLParser
from .verilog_generator import VerilogGenerator

class GraceHDLCompiler:
    """GraceHDL编译器"""
    
    def __init__(self):
        self.lexer = GraceHDLLexer()
        self.parser = GraceHDLParser()
        self.generator = VerilogGenerator()
        
        # 构建解析器
        self.parser.build()
    
    def compile_file(self, input_file, output_file=None):
        """编译GraceHDL文件"""
        try:
            # 读取输入文件
            with open(input_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # 编译
            verilog_code = self.compile_string(source_code)
            
            # 确定输出文件名
            if output_file is None:
                base_name = os.path.splitext(input_file)[0]
                output_file = base_name + '.v'
            
            # 写入输出文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(verilog_code)
            
            print(f"编译成功: {input_file} -> {output_file}")
            return True
            
        except Exception as e:
            print(f"编译失败: {e}")
            return False
    
    def compile_string(self, source_code):
        """编译GraceHDL源代码字符串"""
        try:
            # 语法分析（包含词法分析）
            ast = self.parser.parse(source_code)
            
            # 检查AST是否为空
            if ast is None:
                raise Exception("语法分析失败，无法生成AST")
            
            # 代码生成
            verilog_code = self.generator.generate(ast)
            
            return verilog_code
            
        except Exception as e:
            raise Exception(f"编译错误: {e}")
    
    def check_syntax(self, source_code):
        """检查语法"""
        try:
            # 只进行语法分析
            ast = self.parser.parse(source_code)
            return True, "语法正确"
        except Exception as e:
            return False, f"语法错误: {e}"

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python -m src.compiler <输入文件> [输出文件]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"错误: 文件 {input_file} 不存在")
        sys.exit(1)
    
    compiler = GraceHDLCompiler()
    success = compiler.compile_file(input_file, output_file)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()