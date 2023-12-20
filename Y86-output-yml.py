#!/usr/bin/env python3
# 读取ROM_M.txt和Y86-output.txt文件，将其中的状态转换为Y86-output.yml格式
import os

# 字典 State，用于存储每个状态的值
State = {}
Mem = {}

os.chdir(os.path.dirname(os.path.abspath(__file__)))
output_file = "Y86-output.txt"
with open(output_file, "r") as output_file:
    content = output_file.readlines()

# 从ROM_M.txt读取内存中的指令
txt_Mem_file = "ROM_M.txt"
with open(txt_Mem_file, "r") as txt_Mem_file:
    txt_Mem_content = txt_Mem_file.readlines()
    for line in txt_Mem_content:
        line = line.split()
        Mem[line[1]] = line[2]

yaml_file = output_file.name.replace(".txt", ".yml")
with open(yaml_file, "w") as yaml_content:
    for i in range(2, len(content)):
        line = content[i].split()
        if line[0] == "mem":
            if int(line[2]) == 0:
                continue
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
            # 按照key对应的数字从小到大输出
            for key in sorted(Mem.keys(), key=lambda x: int(x)):
                yaml_content.write("    " + key + ": " + Mem[key] + "\n")

            yaml_content.write("  CC:\n")
            yaml_content.write("    ZF: " + State["ZF"] + "\n")
            yaml_content.write("    SF: " + State["SF"] + "\n")
            yaml_content.write("    OF: " + State["OF"] + "\n")
            yaml_content.write("  STAT: " + State["STAT"] + "\n")
