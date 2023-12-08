module PCIncre (
    input [3:0] icode,
    input [63:0] PCaddress,
    output reg [63:0] valP
);

    always @(*) begin
        case (icode)
            4'h0:  valP = PCaddress;  // halt
            4'h1:  valP = PCaddress + 1;  // nop
            4'h2:  valP = PCaddress + 2;  // rrmovq, cmovXX
            4'h3:  valP = PCaddress + 10;  // irmovq
            4'h4:  valP = PCaddress + 10;  // rmmovq
            4'h5:  valP = PCaddress + 10;  // mrmovq
            4'h6:  valP = PCaddress + 2;  // addq, subq, andq, xorq
            4'h7:  valP = PCaddress + 9;  // jmp, jXX
            4'h8:  valP = PCaddress + 9;  // call
            4'h9:  valP = PCaddress + 1;  // ret
            4'hA: valP = PCaddress + 2;  // pushq
            4'hB: valP = PCaddress + 2;  // popq  
        endcase
    end
endmodule
