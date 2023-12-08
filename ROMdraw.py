#!/usr/bin/env python3
# 读取ROM.yo文件，将其中的指令转换为ROM.txt和ROM_M.txt文件中的指令
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
files = os.listdir(".")
yo_files = [file for file in files if file.endswith(".yo")]

for yo_file in yo_files:
    with open(yo_file, "r") as yo_file:
        yo_content = yo_file.readlines()

    txt_file = yo_file.name.replace(".yo", ".txt")
    with open(txt_file, "w") as txt_file:
        # 首先写入1024行的 00
        txt_content = ["00" for i in range(1024)]

        for line in yo_content:
            # 如果不是有效行，跳过
            if len(line.strip().split("|")[0].strip().split(":")) != 2:
                continue
            # 获取地址和指令
            hex_address = line.strip().split("|")[0].strip().split(":")[0].strip()
            hex_instruction = line.strip().split("|")[0].strip().split(":")[1].strip()
            dec_address = int(hex_address, 16)
            # 在对应地址位置覆盖写入指令
            for i in range(0, int(len(hex_instruction) / 2)):
                txt_content[dec_address + i] = hex_instruction[i * 2 : i * 2 + 2]

        txt_file.write("\n".join(txt_content))

    txt_file = yo_file.name.replace(".yo", ".txt")
    txt_Mem_file = txt_file.replace(".txt", "_M.txt")
    with open(txt_file, "r") as txt_file:
        txt_content = txt_file.readlines()

    # 将txt文件中每行一字节的指令转换为_M.txt文件中每行八字节的指令
    with open(txt_Mem_file, "w") as txt_Mem_file:
        txt_Mem_content = []
        for i in range(0, int(len(txt_content) / 8)):
            # 小端法逆序存储
            txt_Mem_content.append(
                "".join(txt_content[i * 8 : i * 8 + 8][::-1]).replace("\n", "")
            )
            # 将这个64bits的十六进制整数转换为十进制有符号整数
            signed_num = int(txt_Mem_content[i], 16)
            # 如果最高位为1，说明是负数，需要转换为有符号整数
            if signed_num & 0x8000000000000000:
                signed_num = signed_num - 0x10000000000000000
            txt_Mem_content[i] = str(signed_num)
            # 转换为"mem i*8 txt_Mem_content[i]"的形式
            txt_Mem_content[i] = "mem " + str(i * 8) + " " + txt_Mem_content[i]
            # 如果最后那个数字是0，则清空
            if signed_num == 0:
                txt_Mem_content[i] = ""

        # 清除所有空行
        txt_Mem_content = [line for line in txt_Mem_content if line != ""]
        txt_Mem_file.write("\n".join(txt_Mem_content))
