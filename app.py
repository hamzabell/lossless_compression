from flask import Flask, request, jsonify
from huffman  import HuffmanCoding
from rle import RunLengthEncoding
from lzw import LempelZivWelch
from shfano import ShannonCompress
from threading import Thread
import concurrent.futures
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '<h1>Welcome To The Analyzer</h1>'



@app.route('/compress', methods=['POST'])
def upload_file():
    f = request.files['file']
    tag = request.form['tag']
    data = bytes(f.read())
    

    input_file_size = len(data)
    filename, file_extension = os.path.splitext(f.filename)

    if(tag =="huffman"):
        h = HuffmanCoding(data)
        huffman_file_size = h.compress(f.filename)
        return jsonify({
             'success': True,
             'fileSize': input_file_size,
             'HuffmanEncoding': {
                'compressionRatio': huffman_file_size/input_file_size,
                'compressionFactor': input_file_size/huffman_file_size,
                'savingPercentage': (input_file_size - huffman_file_size)/input_file_size,
                'fileSize': huffman_file_size
              },
        })
    if (tag=="shannon"):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            ShannonCompress(data, f.filename)
            shf_file_size = os.path.getsize(filename +".shf")
            os.remove(filename +".shf")
            return jsonify({
                'success': True,
                'fileSize': input_file_size,
                'ShannonFano': {
                    'compressionRatio': shf_file_size/input_file_size,
                    'compressionFactor': input_file_size/shf_file_size,
                    'savingPercentage': (input_file_size - shf_file_size)/input_file_size,
                    'fileSize': shf_file_size
            },
            })
    if (tag=="lempel"):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            LempelZivWelch(data, f.filename, 8)
            lzw_file_size = os.path.getsize(filename +".lzw")
            os.remove(filename +".lzw")
            return jsonify({
                'success': True,
                'fileSize': input_file_size,
                'LempelZivWelch': {
                    'compressionRatio': lzw_file_size/input_file_size,
                    'compressionFactor': input_file_size/lzw_file_size,
                    'savingPercentage': (input_file_size - lzw_file_size)/input_file_size,
                    'fileSize': lzw_file_size
            }
            })
    if(tag=="rle"):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            RunLengthEncoding(data, f.filename)
            rle_file_size = os.path.getsize(filename +".rle")
            os.remove(filename +".rle")
            return jsonify({
                'success': True,
                'fileSize': input_file_size,
                'RunLengthEncoding': {
                    'compressionRatio': rle_file_size/input_file_size,
                    'compressionFactor': input_file_size/rle_file_size,
                    'savingPercentage': (input_file_size - rle_file_size)/input_file_size,
                    'fileSize': rle_file_size
            },
            })
        
        return jsonify({
            'success': False,
            "message": "Please pass a valid tag"
        })

if __name__ == '__main__':
    app.run(debug=True)