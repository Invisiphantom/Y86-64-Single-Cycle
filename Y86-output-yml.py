#!/usr/bin/python3
# 读取ROM.txt和Y86-output.txt文件
# 将其中的CPU和内存状态转换为Y86-output.yml格式
import os
import sys

# 将工作目录切换至当前文件所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 字典State用于存储CPU的状态值
# 字典Mem用于存储内存的值
State = {}
Mem = {}


# 从ROM.txt读取内存中存储的原始指令数据
ROM_file = "ROM.txt"
with open(ROM_file, "r") as ROM_file:
    ROM_content = ROM_file.readlines()
    for i in range(0, int(len(ROM_content) / 8)):
        # 小端法存储的指令需要逆序读取
        hex_line = "".join(ROM_content[i * 8 : i * 8 + 8][::-1])
        hex_line = hex_line.replace("\n", "")
        # 将这个64bits的十六进制整数转换为无符号整数
        signed_num = int(hex_line, 16)
        # 如果最高位为1，需要转换为负数
        if signed_num & 0x8000000000000000:
            signed_num = signed_num - 0x10000000000000000
        if signed_num == 0:
            continue
        # 将这个有符号整数转换为字符串，存储到Mem字典中
        Mem[str(i * 8)] = str(signed_num)


# 从Y86-output.txt中读取CPU的状态值
output_file = "Y86-output.txt"
with open(output_file, "r") as output_file:
    content = output_file.readlines()

# 将CPU和内存的状态写入Y86-output.yml文件中
yaml_file = output_file.name.replace(".txt", ".yml")
with open(yaml_file, "w") as yaml_content:
    for i in range(2, len(content)):
        line = content[i].split()
        # 读取内存每次修改后发生的变化
        if line[0] == "mem":
            try:
                if int(line[2]) == 0:
                    continue
            except ValueError as e:
                print(f"Caught exception: {e}")
                print(line)
                sys.exit(1)
            Mem[line[1]] = line[2]

        if line[0] != "mem":
            State["PC"] = line[0]
            State["rax"] = line[1]
            State["rcx"] = line[2]
            State["rdx"] = line[3]
            State["rbx"] = line[4]
            State["rsp"] = line[5]
            State["rbp"] = line[6]
            State["rsi"] = line[7]
            State["rdi"] = line[8]
            State["r8"] = line[9]
            State["r9"] = line[10]
            State["r10"] = line[11]
            State["r11"] = line[12]
            State["r12"] = line[13]
            State["r13"] = line[14]
            State["r14"] = line[15]
            State["ZF"] = line[16]
            State["SF"] = line[17]
            State["OF"] = line[18]
            State["STAT"] = line[19]
            yaml_content.write("- PC: " + State["PC"] + "\n")
            yaml_content.write("  REG:\n")
            yaml_content.write("    rax: " + State["rax"] + "\n")
            yaml_content.write("    rcx: " + State["rcx"] + "\n")
            yaml_content.write("    rdx: " + State["rdx"] + "\n")
            yaml_content.write("    rbx: " + State["rbx"] + "\n")
            yaml_content.write("    rsp: " + State["rsp"] + "\n")
            yaml_content.write("    rbp: " + State["rbp"] + "\n")
            yaml_content.write("    rsi: " + State["rsi"] + "\n")
            yaml_content.write("    rdi: " + State["rdi"] + "\n")
            yaml_content.write("    r8: " + State["r8"] + "\n")
            yaml_content.write("    r9: " + State["r9"] + "\n")
            yaml_content.write("    r10: " + State["r10"] + "\n")
            yaml_content.write("    r11: " + State["r11"] + "\n")
            yaml_content.write("    r12: " + State["r12"] + "\n")
            yaml_content.write("    r13: " + State["r13"] + "\n")
            yaml_content.write("    r14: " + State["r14"] + "\n")
            yaml_content.write("  MEM:\n")

            # 按照地址从小到大输出内存值
            for address in sorted(Mem.keys(), key=lambda x: int(x)):
                yaml_content.write("    " + address + ": " + Mem[address] + "\n")

            yaml_content.write("  CC:\n")
            yaml_content.write("    ZF: " + State["ZF"] + "\n")
            yaml_content.write("    SF: " + State["SF"] + "\n")
            yaml_content.write("    OF: " + State["OF"] + "\n")
            yaml_content.write("  STAT: " + State["STAT"] + "\n")
