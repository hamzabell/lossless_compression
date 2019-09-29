from flask import jsonify
import os

def RunLengthEncoding(data, input_file):

    output = ''
    sequence = []
    count = 1
    for i, char in enumerate(data):
        next_char = data[i+1:i+2]
        if char != next_char:
            sequence.append({char: count})
            count = 0
        count += 1
    for obj in sequence:
        for k, v in obj.items():
            output += '{0}{1}'.format('' if v == 1 else v, k)


    filename, file_extension = os.path.splitext(input_file)
    output_path = filename + ".rle"

    output_file = open(output_path, "w")
    for data in output:
        output_file.write(data)
        
    output_file.close()

    return True



