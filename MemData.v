module MemData (
    input [3:0] icode,
    input [63:0] valP,
    input [63:0] valA,
    output reg [63:0] memData
);
    always @(*) begin
        case (icode)
            // call
            4'h8: memData = valP;
            // rmmovq, pushq
            4'h4, 4'hA: memData = valA;
        endcase
    end
endmodule
