module pwm_counter;

     wire clk;
     wire reset;
     wire enable;
    
     reg[7:0] count;
     wire pwm_out;
     wire period_complete;
    
    reg[7:0] counter_reg;
    reg[7:0] duty_cycle;
    
    always @(posedge clk)
    begin
        if (reset)
        begin
            counter_reg = 8'd0;
            duty_cycle = 8'd128;
        end
        else
            if (enable)
                if ((counter_reg == 8'd255))
                    counter_reg = 8'd0;
                else
                    counter_reg = (counter_reg + 8'd1);
    end
    
    always_comb
    begin
        count = counter_reg;
        pwm_out = (counter_reg < duty_cycle);
        period_complete = (counter_reg == 8'd255);
    end
    
endmodule
