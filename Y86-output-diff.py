#!/usr/bin/env python3
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

output_path = "./Y86-output"
answer_path = "./Y86-answer"

output_files = os.listdir(output_path)
answer_files = os.listdir(answer_path)

error = False
for output_file in output_files:
    answer_file = output_file.replace(".yml", "")
    with open(os.path.join(output_path, output_file), "r") as output_file_IO:
        output_content = output_file_IO.readlines()
    with open(os.path.join(answer_path, answer_file), "r") as answer_file_IO:
        answer_content = answer_file_IO.readlines()

    if output_content != answer_content:
        error = True
        print(
            "Error: "
            + output_file
            + " is different from "
            + output_file.replace(".yml", "")
        )

if error == False:
    print("All tests passed!")