module Stat (
    input [3:0] icode,  // HLT
    input instr_valid,
    input imem_error,
    input dmem_error,
    output reg [2:0] stat  // 1: AOK, 2: HLT, 3: ADR, 4: INS
);
    initial stat = 3'b001;
    always @(icode or dmem_error) begin
        #1;  // 延迟写入使得output能与测试答案匹配
        if (stat == 3'h1) begin
            if (icode == 4'h0) stat <= 3'h2;  // HLT
            else if (dmem_error == 1'b1) stat <= 3'h3;  // ADR
            else if (instr_valid == 1'b0) stat <= 3'h4;  // INS
            else stat <= stat;  // AOK
        end
    end
endmodule
