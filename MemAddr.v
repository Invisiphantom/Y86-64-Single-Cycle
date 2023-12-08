module MemAddr (
    input [3:0] icode,
    input [63:0] valE,
    input [63:0] valA,
    output reg [63:0] memAddr
);
    always @(*) begin
        case (icode)
            // rmmovq, mrmovq, call, pushq
            4'h4, 4'h5, 4'h8, 4'hA: memAddr <= valE;
            // ret, popq
            4'h9, 4'hB: memAddr <= valA; // (rRsp)
            default: memAddr <= 64'hxxxxxxxxxxxxxxxx;
        endcase
    end
endmodule
