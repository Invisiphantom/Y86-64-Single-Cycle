module ALU_fun (
    input [3:0] icode,
    input [3:0] ifun,
    output reg [1:0] aluFun
);
    always @(*) begin
        case (icode)
            4'h2, 4'h3, 4'h4, 4'h5: aluFun = 2'b00;
            4'h6: aluFun = ifun;
            4'h8, 4'hA: aluFun = 2'b01;
            4'h9, 4'hB: aluFun = 2'b00;
            default: aluFun = aluFun;
        endcase
    end
endmodule
