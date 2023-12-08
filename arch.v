module arch (
    input clk
);

    wire pCnd;
    wire [3:0] pIcode;
    wire [63:0] pValC;
    wire [63:0] pValP;
    wire [63:0] pValM;
    wire [2:0] stat;
    wire [63:0] PCaddress;
    PC u_PC (
        .clk      (clk),
        .pIcode   (pIcode),
        .pCnd     (pCnd),
        .pValC    (pValC),
        .pValP    (pValP),
        .pValM    (pValM),
        .stat     (stat),
        .PCaddress(PCaddress)
    );

    wire [ 3:0] icode;
    wire [ 3:0] ifun;
    wire [ 3:0] rA;
    wire [ 3:0] rB;
    wire [63:0] valC;
    assign pIcode = icode;
    assign pValC  = valC;
    InstMemory u_InstMemory (
        .PCaddress(PCaddress),
        .stat     (stat),
        .icode    (icode),
        .ifun     (ifun),
        .rA       (rA),
        .rB       (rB),
        .valC     (valC)
    );


    wire [63:0] valP;
    assign pValP = valP;
    PCIncre u_PCIncre (
        .icode    (icode),
        .PCaddress(PCaddress),
        .valP     (valP)
    );

    wire Cnd;
    wire [63:0] valE;
    wire [63:0] valM;
    wire [63:0] valA;
    wire [63:0] valB;
    assign pCnd  = Cnd;
    assign pValM = valM;
    wire signed [63:0] rax, rcx, rdx, rbx, rsp, rbp, rsi, rdi, r8, r9, r10, r11, r12, r13, r14;
    Regs u_Regs (
        .clk  (clk),
        .Cnd  (Cnd),
        .icode(icode),
        .rA   (rA),
        .rB   (rB),
        .valE (valE),
        .valM (valM),
        .valA (valA),
        .valB (valB),
        .rax  (rax),
        .rcx  (rcx),
        .rdx  (rdx),
        .rbx  (rbx),
        .rsp  (rsp),
        .rbp  (rbp),
        .rsi  (rsi),
        .rdi  (rdi),
        .r8   (r8),
        .r9   (r9),
        .r10  (r10),
        .r11  (r11),
        .r12  (r12),
        .r13  (r13),
        .r14  (r14)
    );



    wire [1:0] aluFun;
    ALU_fun u_ALU_fun (
        .icode (icode),
        .ifun  (ifun),
        .aluFun(aluFun)
    );

    wire [63:0] aluA;
    ALU_A u_ALU_A (
        .icode(icode),
        .valC (valC),
        .valA (valA),
        .aluA (aluA)
    );

    wire [63:0] aluB;
    ALU_B u_ALU_B (
        .icode(icode),
        .valB (valB),
        .aluB (aluB)
    );

    wire ZF, SF, OF;
    ALU u_ALU (
        .clk   (clk),
        .icode (icode),
        .aluFun(aluFun),
        .aluA  (aluA),
        .aluB  (aluB),
        .valE  (valE),
        .ZF    (ZF),
        .SF    (SF),
        .OF    (OF)
    );

    CC u_CC (
        .ifun(ifun),
        .ZF  (ZF),
        .SF  (SF),
        .OF  (OF),
        .Cnd (Cnd)
    );

    wire memWrite, memRead;
    MemControl u_MemControl (
        .icode   (icode),
        .memWrite(memWrite),
        .memRead (memRead)
    );

    wire [63:0] memAddr;
    MemAddr u_MemAddr (
        .icode  (icode),
        .valE   (valE),
        .valA   (valA),
        .memAddr(memAddr)
    );

    wire [63:0] memData;
    MemData u_MemData (
        .icode  (icode),
        .valP   (valP),
        .valA   (valA),
        .memData(memData)
    );

    wire dmem_error;
    Mem u_Mem (
        .memWrite  (memWrite),
        .memRead   (memRead),
        .memAddr   (memAddr),
        .memData   (memData),
        .valM      (valM),
        .dmem_error(dmem_error)
    );

    wire instr_valid, imem_error;

    Stat u_Stat (
        .icode      (icode),
        .instr_valid(instr_valid),
        .imem_error (imem_error),
        .dmem_error (dmem_error),
        .stat       (stat)
    );
endmodule



module arch_tb;
    reg clk;

    arch arch_inst (.clk(clk));

    initial begin
        $monitor("%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d",
                 arch_tb.arch_inst.PCaddress, arch_tb.arch_inst.rax, arch_tb.arch_inst.rcx,
                 arch_tb.arch_inst.rdx, arch_tb.arch_inst.rbx, arch_tb.arch_inst.rsp,
                 arch_tb.arch_inst.rbp, arch_tb.arch_inst.rsi, arch_tb.arch_inst.rdi,
                 arch_tb.arch_inst.r8, arch_tb.arch_inst.r9, arch_tb.arch_inst.r10,
                 arch_tb.arch_inst.r11, arch_tb.arch_inst.r12, arch_tb.arch_inst.r13,
                 arch_tb.arch_inst.r14, arch_tb.arch_inst.ZF, arch_tb.arch_inst.SF,
                 arch_tb.arch_inst.OF, arch_tb.arch_inst.stat);
        repeat (100) begin
            clk = 0;
            #5;
            clk = 1;
            #5;
        end
        $finish;
    end

    initial begin
        $dumpfile("wave.vcd");
        $dumpvars;
    end
endmodule
