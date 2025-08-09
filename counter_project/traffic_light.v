module traffic_light;

     wire clk;
     wire reset;
     wire sensor;
    
     reg red;
     reg yellow;
     reg green;
     reg[1:0] state;
    
    reg[1:0] current_state;
    reg[7:0] timer;
    
    always @(posedge clk)
    begin
        if (reset)
        begin
            current_state = 2'd0;
            timer = 8'd0;
        end
        else
            if ((timer == 8'd255))
            begin
                timer = 8'd0;
                if ((current_state == 2'd0))
                    current_state = 2'd1;
                else
                    if ((current_state == 2'd1))
                        current_state = 2'd2;
                    else
                        if ((current_state == 2'd2))
                            current_state = 2'd0;
                        else
                            current_state = 2'd0;
            end
            else
                timer = (timer + 8'd1);
    end
    
    always_comb
    begin
        state = current_state;
        if ((current_state == 2'd0))
        begin
            red = 1'b1;
            yellow = 1'b0;
            green = 1'b0;
        end
        else
            if ((current_state == 2'd1))
            begin
                red = 1'b0;
                yellow = 1'b1;
                green = 1'b0;
            end
            else
            begin
                red = 1'b0;
                yellow = 1'b0;
                green = 1'b1;
            end
    end
    
endmodule
