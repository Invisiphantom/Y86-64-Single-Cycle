module Mem (
    input memWrite,
    input memRead,
    input [63:0] memAddr,
    input [63:0] memData,
    output reg [63:0] valM,
    output reg dmem_error
);
    // 总共1024字节的内存空间
    parameter MEM_SIZE = 1024;
    reg [7:0] mem[0:MEM_SIZE-1];
    // 使用ROMreplace.py修改至当前绝对路径
    initial $readmemh("/home/ethan/Y86-64-Single-Cycle/ROM.txt", mem);

    always @(memRead or memWrite or memAddr or memData) begin
        #1;  // 消除memAddr和memData的抖动
        if (memAddr >= MEM_SIZE) dmem_error <= 1'b1;
        else begin
            dmem_error <= 1'b0;
            // 小端法读写内存数据
            if (memRead == 1'b1)
                valM <= {
                    mem[memAddr+7],
                    mem[memAddr+6],
                    mem[memAddr+5],
                    mem[memAddr+4],
                    mem[memAddr+3],
                    mem[memAddr+2],
                    mem[memAddr+1],
                    mem[memAddr]
                };
            else if (memWrite == 1'b1) begin
                {mem[memAddr + 7], mem[memAddr + 6], mem[memAddr + 5], mem[memAddr + 4], mem[memAddr + 3], mem[memAddr + 2], mem[memAddr + 1], mem[memAddr]} <= memData;
                // 打印内存写入信息
                $display("mem %d %d", memAddr, memData);
            end
        end
    end
endmodule
