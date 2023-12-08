module InstMemory (
    input      [63:0] PCaddress,
    input      [ 2:0] stat,
    output reg [ 3:0] icode,
    output reg [ 3:0] ifun,
    output reg [ 3:0] rA,
    output reg [ 3:0] rB,
    output     [63:0] valC
);

    reg [7:0] inst_mem[0:1023];  // 最多能存 1024 字节的指令
    // 只能用绝对路径
    initial $readmemh("/home/ethan/CPU-Table/Y86-64-Single-Cycle/ROM.txt", inst_mem);

    wire [79:0] instruction;
    assign instruction[79:0] = (stat == 3'b001) ? {
        inst_mem[PCaddress],
        inst_mem[PCaddress+1],
        inst_mem[PCaddress+2],
        inst_mem[PCaddress+3],
        inst_mem[PCaddress+4],
        inst_mem[PCaddress+5],
        inst_mem[PCaddress+6],
        inst_mem[PCaddress+7],
        inst_mem[PCaddress+8],
        inst_mem[PCaddress+9]
    } : {80{1'bx}};

    reg [63:0] valC_litend;

    always @(*) begin
        icode = instruction[79:76]; // 4 bits
        ifun  = instruction[75:72]; // 4 bits
        rA    = instruction[71:68]; // 4 bits
        rB    = instruction[67:64]; // 4 bits

        case (icode)
            4'd3, 4'd4, 4'd5: valC_litend = instruction[63:0];  // irmovq, rmmovq, mrmovq
            4'd7, 4'd8: valC_litend = instruction[71:8];  // jmp, jXX, call
            default: valC_litend = {64{1'b0}};
        endcase
    end

    // 小端法读取数据
    assign valC = {
        valC_litend[7:0],
        valC_litend[15:8],
        valC_litend[23:16],
        valC_litend[31:24],
        valC_litend[39:32],
        valC_litend[47:40],
        valC_litend[55:48],
        valC_litend[63:56]
    };
endmodule
