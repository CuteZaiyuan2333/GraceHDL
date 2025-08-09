#!/usr/bin/env python3
"""
GraceHDL编译器主程序
将GraceHDL代码编译为Verilog HDL代码
"""

import argparse
import sys
import os
from pathlib import Path
from colorama import init, Fore, Style

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.lexer import GraceHDLLexer
from src.parser import GraceHDLParser
from src.verilog_generator import VerilogGenerator

# 初始化colorama
init()

class GraceHDLCompiler:
    """GraceHDL编译器"""
    
    def __init__(self):
        self.lexer = GraceHDLLexer()
        self.lexer.build()
        self.parser = GraceHDLParser()
        self.parser.build(debug=False)
        self.generator = VerilogGenerator()

    def compile_file(self, input_file, output_file=None, verbose=False):
        """编译单个文件"""
        try:
            # 读取输入文件
            with open(input_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            if verbose:
                print(f"{Fore.BLUE}正在编译: {input_file}{Style.RESET_ALL}")
            
            # 词法分析
            if verbose:
                print(f"{Fore.YELLOW}词法分析中...{Style.RESET_ALL}")
            
            # 语法分析
            if verbose:
                print(f"{Fore.YELLOW}语法分析中...{Style.RESET_ALL}")
            
            # 设置词法分析器输入
            self.lexer.input(source_code)
            ast = self.parser.parser.parse(source_code, lexer=self.lexer, debug=False)
            
            if ast is None:
                print(f"{Fore.RED}语法分析失败{Style.RESET_ALL}")
                return False
            
            # 代码生成
            if verbose:
                print(f"{Fore.YELLOW}生成Verilog代码中...{Style.RESET_ALL}")
            
            verilog_code = self.generator.generate(ast)
            
            # 确定输出文件名
            if output_file is None:
                input_path = Path(input_file)
                output_file = input_path.with_suffix('.v')
            
            # 写入输出文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(verilog_code)
            
            if verbose:
                print(f"{Fore.GREEN}编译成功: {output_file}{Style.RESET_ALL}")
            
            return True
            
        except FileNotFoundError:
            print(f"{Fore.RED}错误: 找不到文件 '{input_file}'{Style.RESET_ALL}")
            return False
        except Exception as e:
            print(f"{Fore.RED}编译错误: {str(e)}{Style.RESET_ALL}")
            return False

    def compile_directory(self, input_dir, output_dir=None, verbose=False):
        """编译目录中的所有.ghdl文件"""
        input_path = Path(input_dir)
        if not input_path.is_dir():
            print(f"{Fore.RED}错误: '{input_dir}' 不是一个目录{Style.RESET_ALL}")
            return False
        
        # 查找所有.ghdl文件
        ghdl_files = list(input_path.glob('**/*.ghdl'))
        
        if not ghdl_files:
            print(f"{Fore.YELLOW}警告: 在 '{input_dir}' 中没有找到.ghdl文件{Style.RESET_ALL}")
            return True
        
        if verbose:
            print(f"{Fore.BLUE}找到 {len(ghdl_files)} 个.ghdl文件{Style.RESET_ALL}")
        
        success_count = 0
        
        for ghdl_file in ghdl_files:
            # 确定输出文件路径
            if output_dir:
                output_path = Path(output_dir)
                relative_path = ghdl_file.relative_to(input_path)
                output_file = output_path / relative_path.with_suffix('.v')
                output_file.parent.mkdir(parents=True, exist_ok=True)
            else:
                output_file = ghdl_file.with_suffix('.v')
            
            if self.compile_file(str(ghdl_file), str(output_file), verbose):
                success_count += 1
        
        print(f"{Fore.GREEN}编译完成: {success_count}/{len(ghdl_files)} 个文件成功{Style.RESET_ALL}")
        return success_count == len(ghdl_files)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='GraceHDL编译器 - 将GraceHDL代码编译为Verilog HDL',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s input.ghdl                    # 编译单个文件
  %(prog)s input.ghdl -o output.v        # 指定输出文件
  %(prog)s src/ -d build/                # 编译目录
  %(prog)s input.ghdl -v                 # 详细输出
        """
    )
    
    parser.add_argument('input', help='输入文件或目录')
    parser.add_argument('-o', '--output', help='输出文件（仅用于单文件编译）')
    parser.add_argument('-d', '--output-dir', help='输出目录（用于目录编译）')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    parser.add_argument('--version', action='version', version='GraceHDL Compiler 1.0.0')
    
    args = parser.parse_args()
    
    # 创建编译器实例
    compiler = GraceHDLCompiler()
    
    # 检查输入是文件还是目录
    input_path = Path(args.input)
    
    if input_path.is_file():
        # 编译单个文件
        success = compiler.compile_file(args.input, args.output, args.verbose)
    elif input_path.is_dir():
        # 编译目录
        if args.output:
            print(f"{Fore.YELLOW}警告: 目录编译时忽略 -o 选项，请使用 -d{Style.RESET_ALL}")
        success = compiler.compile_directory(args.input, args.output_dir, args.verbose)
    else:
        print(f"{Fore.RED}错误: '{args.input}' 不存在{Style.RESET_ALL}")
        success = False
    
    # 返回适当的退出码
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()