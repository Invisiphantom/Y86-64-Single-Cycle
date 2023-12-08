module Stat (
    input [3:0] icode,  // HLT
    input instr_valid,
    input imem_error,
    input dmem_error,
    output reg [2:0] stat // 1: AOK, 2: HLT, 3: ADR, 4: INS
);
    initial stat = 3'b001;
    always @(icode or dmem_error) begin
        #1;
        if (icode == 4'h0) stat <= 3'h2;
        else if (dmem_error == 1'b1) stat <= 3'h3;
        else stat <= stat;
    end
endmodule
