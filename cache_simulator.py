#32 sets, 1-way set associative (Direct mapped)
#8 contingous addresses per line
#each memory reference is a 3 byte word
#

import math

def main():
    data = []
    N = 32 # number of sets
    K = 4 # number of lines(blocks) per set
    L = 8 # number of bytes per line(block) of cache mem

    HIT = 0
    MISS = 0

    #Read memory references from trace file and store every byte as a string of bits in a list
    #Currently using TRACE1.DAT -> change for trace file as neccesary
    with open("traceFiles/TRACE1.DAT", "rb") as file:
        byte = file.read(1)
        while byte:
            byte = ord(byte)#converting byte to unicode prior to binary convert
            byte = bin(byte)[2:].rjust(8, '0')#padding bits with 0s
            data.append(byte) #add converted byte to list
            byte = file.read(1)

    reorderedData = []
    i = 0

    #reorder bits
    while i < len(data) - 2:
        reorderedData.append(data[i+2] + data[i+1] + data[i]) #reordering
        i += 3


    #get ready to hold the data as a list of objects, keep track of the offsets
    dataSets = [] 
    indexes = []

    #lower 3 bits are cleared so, ignore bits 21-23
    for entry in reorderedData:
        index_size = int(math.log2(K)) # 1,2,3,4
        index_start = 21 - index_size
        index = entry[index_start:21] #21 is stop bit, not included
        #print(index)
        indexes.append(index)

        # offset = entry[:]
        # offsets.append(offset)
        #offset probably not used due to removal of last 3 bits,
        #as stated in handout

        tag = entry[0:index_start] #setting tag
        dataSet = Sets(tag, index)
        dataSets.append(dataSet)

    print(dataSets[0])


#"Sets" class for the cache
#Sets are comprised of the tags, index, and offset
#easiest to define it as an object with parameters
class Sets(object):
    tag = "" #data
    index = [] #* 16 #address within set
    #offset = "" #index within block

    def __init__(self, tag, index):
        self.tag = tag
        self.index = index
		
        

main()