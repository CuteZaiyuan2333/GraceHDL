module decoder_simple;

     wire[2:0] addr;
    
     wire[7:0] out;
    
    always_comb
    begin
        case (addr)
            3'd0:
                out = 8'd1;
            3'd1:
                out = 8'd2;
            default:
                out = 8'd0;
        endcase
    end
    
endmodule
