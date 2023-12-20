#!/usr/bin/python3
# 读取ROM.yo文件中的内容，裁剪其中的十六进制汇编指令生成ROM.txt文件
import os

# 将工作目录切换至当前文件所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


files = os.listdir(".")
yo_files = [file for file in files if file.endswith(".yo")]

for yo_file in yo_files:
    with open(yo_file, "r") as yo_file:
        yo_content = yo_file.readlines()

    txt_file = yo_file.name.replace(".yo", ".txt")
    with open(txt_file, "w") as txt_file:
        # 首先写入1024行的 00
        ROM_content = ["00" for _ in range(1024)]

        for line in yo_content:
            # 取出每行的地址和指令部分
            add_inst = line.split("|")[0].split(":")
            # 如果不是有效行(由":"分割地址和指令)，则跳过
            if len(add_inst) != 2:
                continue
            # 获取地址和指令
            hex_address = add_inst[0].strip()
            hex_instruction = add_inst[1].strip()
            dec_address = int(hex_address, 16)
            # 在ROM_content中的对应地址位置覆盖写入指令
            for i in range(0, int(len(hex_instruction) / 2)):
                ROM_content[dec_address + i] = hex_instruction[i * 2 : i * 2 + 2]

        txt_file.write("\n".join(ROM_content))
