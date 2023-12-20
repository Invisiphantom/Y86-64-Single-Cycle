#!/usr/bin/env python3
# 将InstMemory.v和Mem.v中$readmemh()的ROM.txt路径替换为当前的绝对路径
import os
import re

# 将工作目录切换至当前文件所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("InstMemory.v", "r") as file:
    content = file.read()
content = re.sub(
    r'\$readmemh\(".*?ROM\.txt", inst_mem\);',
    f'$readmemh("{os.getcwd()}/ROM.txt", inst_mem);',
    content,
)
with open("InstMemory.v", "w") as file:
    file.write(content)

with open("Mem.v", "r") as file:
    content = file.read()
content = re.sub(
    r'\$readmemh\(".*?ROM\.txt", inst_mem\);',
    f'$readmemh("{os.getcwd()}/ROM.txt", inst_mem);',
    content,
)
with open("Mem.v", "w") as file:
    file.write(content)
