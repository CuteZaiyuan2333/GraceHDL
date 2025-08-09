module simple_test;

     wire clk;
     wire reset;
    
     reg out;
    
    reg result;
    
    always @(posedge clk)
    begin
        if (reset)
            result = 1'b0;
        else
            result = 1'b1;
    end
    
    always_comb
    begin
        out = result;
    end
    
endmodule
