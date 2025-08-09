# GraceHDL 基本门电路展示

# 展示基本的组合逻辑门设计


# 与门

module and_gate(
    input wire a,
    input wire b,
    output wire y
);

    assign y = (a & b);
    # 或门
    
endmodule

module or_gate(
    input wire a,
    input wire b,
    output wire y
);

    assign y = (a | b);
    # 非门
    
endmodule

module not_gate(
    input wire a,
    output wire y
);

    assign y = (~a);
    # 异或门
    
endmodule

module xor_gate(
    input wire a,
    input wire b,
    output wire y
);

    assign y = (a ^ b);
    # 全加器
    
endmodule

module full_adder(
    input wire a,
    input wire b,
    input wire cin,
    output wire sum,
    output wire cout
);

    assign sum = (a ^ (b ^ cin));
    assign cout = ((a & b) | (cin & (a ^ b)));
    # 4位与门阵列
    
endmodule

module and_array_4bit(
    input wire[3:0] a,
    input wire[3:0] b,
    output wire[3:0] y
);

    assign y = (a & b);
    # 2选1多路选择器
    
endmodule

module mux_2to1(
    input wire a,
    input wire b,
    input wire sel,
    output wire y
);

    assign y = ((~(sel & a)) | (sel & b));
    # 3-8译码器
    
endmodule

module decoder_3to8(
    input wire[2:0] addr,
    output reg[7:0] out
);

    always @(*)
    begin
        case (addr)
            3'd0:
                out = 8'd1;
            3'd1:
                out = 8'd2;
            3'd2:
                out = 8'd4;
            3'd3:
                out = 8'd8;
            3'd4:
                out = 8'd16;
            3'd5:
                out = 8'd32;
            3'd6:
                out = 8'd64;
            3'd7:
                out = 8'd128;
            default:
                out = 8'd0;
        endcase
    end
    
endmodule
