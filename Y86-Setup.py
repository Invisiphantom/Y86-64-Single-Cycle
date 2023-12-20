#!/usr/bin/env python3
# 脚本功能：批量测试Y86程序
import os
import shutil

# 将工作目录切换至当前文件所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

test_path = "./test"
yo_files = os.listdir(test_path)

# 清空output_path文件夹中的内容
output_path = "./Y86-output"
shutil.rmtree(output_path)
os.mkdir(output_path)

# 将InstMemory.v和Mem.v中的$readmemh()路径替换为当前目录下的绝对路径
os.system("python3 -u ROMpath.py")

# 对test中的每个测试文件进行测试，并将仿真结果保存到Y86-output文件夹中
for yo_file in yo_files:
    # 将test文件夹中的测试文件复制到当前目录下的ROM.yo
    with open(os.path.join(test_path, yo_file), "r") as yo_file_IO:
        yo_content = yo_file_IO.readlines()
    with open("ROM.yo", "w") as ROM_file:
        ROM_file.write("".join(yo_content))

    # 读取ROM.yo文件，裁剪其中的十六进制指令后生成`ROM.txt`文件
    os.system("python3 -u ROMgen.py")
    # 执行仿真，并将输出结果写入Y86-output.txt文件
    os.system(
        "iverilog -y $PWD arch.v -o bin/arch && cd bin && rm -f *.vcd && vvp arch > ../Y86-output.txt && rm arch && cd .."
    )
    # 读取ROM_M.txt和Y86-output.txt文件，将其中的CPU状态转换为Y86-output.yml格式
    os.system("python3 -u Y86-output-yml.py")

    # 将Y86-output.yml文件重命名后移动到Y86-output文件夹中
    with open("Y86-output.yml", "r") as yml_file:
        yml_content = yml_file.readlines()
    with open(
        os.path.join(output_path, yo_file.replace(".yo", ".yml")), "w"
    ) as yml_file:
        yml_file.write("".join(yml_content))

    # 移除之前生成的中间文件
    os.system("rm -f ROM.txt ROM_M.txt Y86-output.txt Y86-output.yml")

# 使用`Y86-output-check.py`逐个比较文件夹`Y86-output`和`Y86-answer`中的每个文件
os.system("python3 -u Y86-output-check.py")
