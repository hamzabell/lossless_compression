import sys
import os


def shannon_fano_encoder(iA, iB, tupleList): # iA to iB : index interval
    size = iB - iA + 1
    if size > 1:
  
        mid = int(size / 2 + iA)
        for i in range(iA, iB + 1):
            tup = tupleList[i]
            if i < mid: # top group
                tupleList[i] = (tup[0], tup[1], tup[2] + '0')
            else: # bottom group
                tupleList[i] = (tup[0], tup[1], tup[2] + '1')
        shannon_fano_encoder(iA, mid - 1, tupleList)
        shannon_fano_encoder(mid, iB, tupleList)

def byteWriter(bitStr, outputFile):
    bitStream = ''
    bitStream += bitStr
    while len(bitStream) > 8: 
        byteStr = bitStream[:8]
        bitStream = bitStream[8:]
        outputFile.write(bytes(chr(int(byteStr, 2)), encoding='utf8'))

def bitReader(n):
    global byteArr
    global bitPosition
    bitStr = ''
    for i in range(n):
        bitPosInByte = 7 - (bitPosition % 8)
        bytePosition = int(bitPosition / 8)
        byteVal = byteArr[bytePosition]
        bitVal = int(byteVal / (2 ** bitPosInByte)) % 2
        bitStr += str(bitVal)
        bitPosition += 1 # prepare to read the next bit
    return bitStr

def ShannonCompress(data, name):
    filename, file_extension = os.path.splitext(name)
    outputFile = filename + ".shf"
    fi = data
    fileSize = len(fi)
    byteArr = bytearray(fi)
    fileSize = len(byteArr)


    freqList = [0] * 256
    for b in byteArr:
        freqList[b] += 1

    tupleList = []
    for b in range(256):
        if freqList[b] > 0:
            tupleList.append((freqList[b], b, ''))

    tupleList = sorted(tupleList, key=lambda tup: tup[0], reverse = True)

    shannon_fano_encoder(0, len(tupleList) - 1, tupleList)

    dic = dict([(tup[1], tup[2]) for tup in tupleList])
    del tupleList 
    bitStream = ''
    fo = open(outputFile, 'wb')
    fo.write(bytes(chr(len(dic) - 1), encoding='utf8')) 
    for (byteValue, encodingBitStr) in dic.items():
        bitStr = bin(byteValue)
        bitStr = bitStr[2:] 
        bitStr = '0' * (8 - len(bitStr)) + bitStr 
        byteWriter(bitStr, fo)
        bitStr = bin(len(encodingBitStr) - 1) 
        bitStr = bitStr[2:] 
        bitStr = '0' * (3 - len(bitStr)) + bitStr 
        byteWriter(bitStr, fo)
        byteWriter(encodingBitStr, fo)

    bitStr = bin(fileSize - 1)
    bitStr = bitStr[2:] 
    bitStr = '0' * (32 - len(bitStr)) + bitStr 
    byteWriter(bitStr, fo)

    for b in byteArr:
        byteWriter(dic[b], fo)

    byteWriter('0' * 8, fo)
    fo.close()
    return True
