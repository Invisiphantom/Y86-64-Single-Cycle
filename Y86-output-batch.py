#!/usr/bin/env python3
import os
import shutil

os.chdir(os.path.dirname(os.path.abspath(__file__)))

test_path = "./test"
yo_files = os.listdir(test_path)

# 清空output_path文件夹中的内容
output_path = "./Y86-output"
shutil.rmtree(output_path)
os.mkdir(output_path)

# 将InstMemory.v和Mem.v中$readmemh()的ROM.txt路径替换为当前的绝对路径
os.system("python3 -u ROMreplace.py")

# 对每个测试文件进行测试，并将结果保持到Y86-output文件夹中
for yo_file in yo_files:
    # 将test文件夹中的测试文件复制到当前目录下
    with open(os.path.join(test_path, yo_file), "r") as yo_file_IO:
        yo_content = yo_file_IO.readlines()
        
    with open("ROM.yo", "w") as ROM_file:
        ROM_file.write("".join(yo_content))

    # 移除之前生成的文件
    os.system("rm -f ROM.txt ROM_M.txt Y86-output.txt Y86-output.yml")
    # 读取ROM.yo文件，将其中的汇编指令转换为ROM.txt和ROM_M.txt文件中的字节编码
    os.system("python3 -u ROMdraw.py")
    # 执行仿真，并将输出结果写入Y86-output.txt文件
    os.system("iverilog -y $PWD arch.v -o bin/arch && cd bin && rm -f *.vcd && vvp arch > ../Y86-output.txt && rm arch && cd ..")
    # 读取ROM_M.txt和Y86-output.txt文件，将其中的状态转换为Y86-output.yml格式
    os.system('python3 -u Y86-output.py')
    
    # 将Y86-output.yml文件中的内容保存到Y86-output文件夹中
    with open("Y86-output.yml", "r") as yml_file:
        yml_content = yml_file.readlines()

    with open(os.path.join(output_path, yo_file.replace(".yo", ".yml")), "w") as yml_file:
        yml_file.write("".join(yml_content))

# 比较Y86-output文件夹和Y86-answer文件夹中的内容是否相同
os.system('python3 -u Y86-output-diff.py')