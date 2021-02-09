#32 sets, 1-way set associative (Direct mapped)
# 8 contingous addresses per line
#each memory reference is a 3 byte word
#

def main():
    data = []
    N = 32
    K = 2
    L = 8

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
    print(reorderedData[0])

    dataObjects 



#"Sets" class for the cache
#Sets are comprised of the tags, index, and offset
#easiest to define it as an object with parameters
class Sets(object):
    tag = "" #data
	index = [""] * 16 #which address within the set 
	offset = "" #set index to go to

	def __init__(self, offset, index, tag):
        self.tag = tag
		self.offset = offset
		self.index = index
		
        

main()