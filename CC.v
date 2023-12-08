module CC (
    input [3:0] ifun,
    input ZF,
    input SF,
    input OF,
    output reg Cnd
);
    always @(*) begin
        case (ifun)
            4'h0: Cnd = 1'b1;  // all
            4'h1: Cnd = (ZF == 1 || SF != OF) ? 1'b1 : 1'b0;  // le
            4'h2: Cnd = (SF != OF) ? 1'b1 : 1'b0;  // l
            4'h3: Cnd = (ZF == 1) ? 1'b1 : 1'b0;  // e
            4'h4: Cnd = (ZF == 0) ? 1'b1 : 1'b0;  // ne
            4'h5: Cnd = (SF == OF) ? 1'b1 : 1'b0;  // ge
            4'h6: Cnd = (ZF == 0 && SF == OF) ? 1'b1 : 1'b0;  // g
            default: Cnd = 1'b0;
        endcase
    end
endmodule
