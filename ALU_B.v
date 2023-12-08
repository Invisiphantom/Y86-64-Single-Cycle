module ALU_B (
    input [3:0] icode,
    input [63:0] valB,  // rmmovq, mrmovq, ops
    output reg [63:0] aluB
);

    always @(*) begin
        case (icode)
            // rrmovq(rA+0), irmovq(valC+0) 
            4'h2, 4'h3: aluB = {64{1'b0}};
            // rmmovq, mrmovq, ops
            4'h4, 4'h5, 4'h6: aluB = valB;
            // call, ret, pushq, popq
            4'h8, 4'h9, 4'hA, 4'hB: aluB = valB;
            default: aluB = aluB;
        endcase
    end
endmodule
