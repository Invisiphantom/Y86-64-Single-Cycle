#!/usr/bin/python3
# 将InstMemory.v和Mem.v中$readmemh()的ROM.txt路径替换为当前的绝对路径
import os
import re

# 将工作目录切换至当前文件所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 替换InstMemory.v中的$readmemh()路径
with open("InstMemory.v", "r") as file:
    content = file.read()
content = re.sub(
    r'\$readmemh\(".*?ROM\.txt", inst_mem\);',
    f'$readmemh("{os.getcwd()}/ROM.txt", inst_mem);',
    content,
)
with open("InstMemory.v", "w") as file:
    file.write(content)

# 替换Mem.v中的$readmemh()路径
with open("Mem.v", "r") as file:
    content = file.read()
content = re.sub(
    r'\$readmemh\(".*?ROM\.txt", mem\);',
    f'$readmemh("{os.getcwd()}/ROM.txt", mem);',
    content,
)
with open("Mem.v", "w") as file:
    file.write(content)
