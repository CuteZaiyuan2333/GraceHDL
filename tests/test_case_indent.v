module decoder_3to8(
    input wire[2:0] addr,
    output reg[7:0] out
);

    always @(*)
    begin
        case (addr)
            3'd0:
                out = 8'd1;
            default:
                out = 8'd0;
        endcase
    end
    
endmodule
