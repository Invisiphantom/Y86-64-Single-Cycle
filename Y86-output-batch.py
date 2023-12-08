#!/usr/bin/env python3
import os
import shutil

os.chdir(os.path.dirname(os.path.abspath(__file__)))

test_path = "./test"
yo_files = os.listdir(test_path)

output_path = "./Y86-output"
# 清空output_path文件夹中的内容
shutil.rmtree(output_path)
os.mkdir(output_path)

for yo_file in yo_files:
    with open(os.path.join(test_path, yo_file), "r") as yo_file_IO:
        yo_content = yo_file_IO.readlines()
        
    with open("ROM.yo", "w") as ROM_file:
        ROM_file.write("".join(yo_content))
    
    os.system("rm -f ROM.txt ROM_M.txt Y86-output.txt Y86-output.yml")
    os.system("python3 -u ROMdraw.py")
    os.system("iverilog -y $PWD arch.v -o bin/arch && cd bin && rm -f *.vcd && vvp arch > ../Y86-output.txt && rm arch && cd ..")
    os.system('python3 -u Y86-output.py')
    
    with open("Y86-output.yml", "r") as yml_file:
        yml_content = yml_file.readlines()
        
    with open(os.path.join(output_path, yo_file.replace(".yo", ".yml")), "w") as yml_file:
        yml_file.write("".join(yml_content))

os.system('python3 -u Y86-output-diff.py')