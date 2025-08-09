# GraceHDL 基本门电路展示

# 展示基本的组合逻辑门设计


# 与门

module and_gate(
    input wire a,
    input wire b,
    output wire y
);

    assign y = (a & b);
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
