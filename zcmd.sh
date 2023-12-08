rm -f ROM.txt ROM_M.txt Y86-output.txt Y86-output.yml
python3 -u ROMdraw.py
iverilog -y $PWD arch.v -o bin/arch && cd bin && rm -f *.vcd && vvp arch > ../Y86-output.txt && rm arch && cd ..
python3 -u Y86-output.py
cd bin && gtkwave wave.vcd && cd ..