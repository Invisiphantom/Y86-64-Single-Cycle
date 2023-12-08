module PC (
    input             clk,
    input      [ 3:0] pIcode,
    input             pCnd,      // jXX 判断是否启用
    input      [63:0] pValM,     // ret
    input      [63:0] pValC,     // jmp jXX call
    input      [63:0] pValP,     // normal PC update
    input      [ 2:0] stat,      // 1: AOK, 2: HLT, 3: ADR, 4: INS
    output reg [63:0] PCaddress
);

    initial PCaddress = {64{1'b0}};

    always @(posedge clk) begin
        if (stat != 3'b001) PCaddress <= PCaddress;
        else
            case (pIcode)
                4'h0: PCaddress <= pValP;  // halt
                4'h1: PCaddress <= pValP;  // nop
                4'h2: PCaddress <= pValP;  // rrmovq, cmovXX
                4'h3: PCaddress <= pValP;  // irmovq
                4'h4: PCaddress <= pValP;  // rmmovq
                4'h5: PCaddress <= pValP;  // mrmovq
                4'h6: PCaddress <= pValP;  // addq, subq, andq, xorq

                4'h7: PCaddress <= pCnd ? pValC : pValP;  // jmp, jXX
                4'h8: PCaddress <= pValC;  // call
                4'h9: PCaddress <= pValM;  // ret

                4'hA: PCaddress <= pValP;  // pushq
                4'hB: PCaddress <= pValP;  // popq
            endcase
    end
endmodule
