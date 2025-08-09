module advanced_counter;

     wire clk;
     wire reset;
     wire enable;
     wire up_down;
    
     reg[7:0] count;
     wire overflow;
     wire underflow;
    
    reg[7:0] counter_reg;
    
    always @(posedge clk)
    begin
        if (reset)
            counter_reg = 8'd0;
        else
            if (enable)
                if (up_down)
                    if ((counter_reg == 8'd255))
                        counter_reg = 8'd0;
                    else
                        counter_reg = (counter_reg + 8'd1);
                else
                    if ((counter_reg == 8'd0))
                        counter_reg = 8'd255;
                    else
                        counter_reg = (counter_reg - 8'd1);
    end
    
    always_comb
    begin
        count = counter_reg;
        overflow = ((counter_reg == 8'd255) & (up_down & enable));
        underflow = ((counter_reg == 8'd0) & enable);
    end
    
endmodule
