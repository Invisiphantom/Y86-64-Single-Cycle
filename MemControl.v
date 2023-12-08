module MemControl (
    input [3:0] icode,
    output reg memWrite,
    output reg memRead
);
    always @(icode) begin
        case (icode)
            4'h4, 4'h8, 4'hA: begin
                memWrite = 1'b1;
                memRead  = 1'b0;
            end
            4'h5, 4'h9, 4'hB: begin
                memWrite = 1'b0;
                memRead  = 1'b1;
            end
            default: begin
                memWrite = 1'b0;
                memRead  = 1'b0;
            end
        endcase
    end
endmodule
