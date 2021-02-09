def main():
    data = []
    N = 32
    K = 2

    HIT = 0
    MISS = 0

    #Read file stream and store every byte as a string of bits in a list
    #File stream used for this example is TRACE2.DAT -> change for various trace files as such
    with open("traceFiles/TRACE1.DAT", "rb") as file:
        byte = file.read(1)
        while byte:
            byte = ord(byte)#converting byte to unicode prior to binary convert
            byte = bin(byte)[2:].rjust(8, '0')#padding bits with 0s
            data.append(byte)
            byte = file.read(1)

    reorderedData = []
    i = 0

    #reorder bits
    while i < len(data) - 2:
        reorderedData.append(data[i+2] + data[i+1] + data[i])
        i += 3
    print(reorderedData[0])
        

main()