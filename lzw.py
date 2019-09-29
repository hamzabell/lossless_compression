import sys
from sys import argv
from struct import *
from flask import jsonify
import os



def LempelZivWelch(inputFile, input_file,  n): 
    filename, file_extension = os.path.splitext(input_file)
    data = str(inputFile)
    maximum_table_size = pow(2,int(n))      
    output_path = filename + ".lzw"      

    dictionary_size = 256                   
    dictionary = {chr(i): i for i in range(dictionary_size)}    
    string = ""             
    compressed_data = []    

    for symbol in data:                     
        string_plus_symbol = string + symbol
        if string_plus_symbol in dictionary: 
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if(len(dictionary) <= maximum_table_size):
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = symbol

    if string in dictionary:
        compressed_data.append(dictionary[string])

    
    output_file = open(output_path, "wb")
    for data in compressed_data:
        output_file.write(bytes(str(data), encoding='utf8'))
        
    output_file.close()

    return True
