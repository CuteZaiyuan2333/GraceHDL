# GraceHDL 基本门电路展示

# 展示基本的组合逻辑门设计


# 与门

module and_gate;

     wire a;
     wire b;
    
     wire y;
    
    assign y = (a & b);
    # 或门
    
endmodule

module or_gate;

     wire a;
     wire b;
    
     wire y;
    
    assign y = (a | b);
    # 非门
    
endmodule

module not_gate;

     wire a;
    
     wire y;
    
    assign y = (~a);
    # 异或门
    
endmodule

module xor_gate;

     wire a;
     wire b;
    
     wire y;
    
    assign y = (a ^ b);
    # 全加器
    
endmodule

module full_adder;

     wire a;
     wire b;
     wire cin;
    
     wire sum;
     wire cout;
    
    assign sum = (a ^ (b ^ cin));
    assign cout = ((a & b) | (cin & (a ^ b)));
    # 4位与门阵列
    
endmodule

module and_array_4bit;

     wire[3:0] a;
     wire[3:0] b;
    
     wire[3:0] y;
    
    assign y = (a & b);
    # 2选1多路选择器
    
endmodule

module mux_2to1;

     wire a;
     wire b;
     wire sel;
    
     wire y;
    
    assign y = ((~(sel & a)) | (sel & b));
    
endmodule
