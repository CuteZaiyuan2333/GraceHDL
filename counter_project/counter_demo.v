module counter_demo;

     wire clk;
     wire reset_btn;
     wire mode_switch;
    
     reg[7:0] display_count;
     wire led_overflow;
     wire led_zero;
    
    reg enable_counter;
    reg[7:0] preset_value;
    reg load_preset;
    reg[3:0] demo_state;
    
    always @(posedge clk)
    begin
        if ((reset_btn == 1'b0))
        begin
            demo_state = 4'd0;
            enable_counter = 1'b1;
            preset_value = 8'd100;
            load_preset = 1'b0;
        end
        else
            if ((demo_state < 4'd15))
                demo_state = (demo_state + 4'd1);
            else
            begin
                demo_state = 4'd0;
                if ((demo_state == 4'd5))
                    load_preset = 1'b1;
                else
                    load_preset = 1'b0;
            end
    end
    
    always_comb
    begin
        display_count = preset_value;
        led_overflow = (demo_state > 4'd10);
        led_zero = (demo_state == 4'd0);
    end
    
endmodule
