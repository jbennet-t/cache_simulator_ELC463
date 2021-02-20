#32 sets, 1-way set associative (Direct mapped)
#8 contingous addresses per line
#each memory reference is a 3 byte word
#

import math

def main():
    data = []
    KN = 64
    K = 4 # number of lines(blocks) per set
    N = int(KN/K) # number of sets
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
    #changing the msb to lsb and vice versa
    while i < len(data) - 2:
        reorderedData.append(data[i+2] + data[i+1] + data[i]) #reordering
        i += 3


    #get ready to hold the data as a list of objects, keep track of the offsets
    #dataSets = [] 
    #indexes = []

    #lower 3 bits are cleared so, ignore bits 21-23

    index_size = int(math.log2(K)) # 1,2,3,4
    index_start = 21 - index_size
    #index = entry[index_start:21] #21 is stop bit, not included
    #print(index)

    # offset = entry[:]
    # offsets.append(offset)
    #offset probably not used due to removal of last 3 bits,
    #as stated in handout

    #tag = entry[0:index_start] #setting tag
    # dataSet = Sets(tag, index)
    # dataSets.append(dataSet)
    #validBit = entry[0]
    
    #print(tag)


    #creating the cache
    # cache = []
    # i = 0
    # while i < N:
    #     cache.append(Sets([""]*K),"")
    #     i += 1
    #     # print(cache[i-1].tag)
    #     # print(dataSets[i-1].tag)

    #     #[ idx  00 01 10 11  cntr
    #     # set 1['a','b','c','d', x]
    #     # set 2['','','','', x]
    #     # set 3['','','','', x]
    #     # set 4['','','','', x]
    #     #]

    #     # 01_a 00_b 11_a 01_a 00_c

    #creating cache 2, electric boogaloo

    cache = []
    idx = 2**index_size

    for i in range(idx):
        col = []
        col.append("%s" %(bin(i)[2:].zfill(index_size))) #convert i to binary index val, remove '0b' prefix
        for j in range(int(N+1)):
            col.append(0)
        cache.append(col)

   # print('[%s]' % ', '.join(map(str, cache)))

    print(cache[0][0])

        

    #-------------------------------------------------------------
    #LRU
    #-------------------------------------------------------------
    for entry in reorderedData:
        for cacheItem in cache:
            for i in range(N):
                set_cntr = 0 #variable for counting spot in set
                if cacheItem[i][0] == entry[index_start:21]: #if the index of the trace data == the index of the cache
                    if cacheItem[i][set_cntr] == 0: #if the space is empty
                        cacheItem[i][set_cntr] = entry[0:index_start] #fill empty space with tag
                        MISS += 1
                        set_cntr += 1 #increment spot in set since its filled
                        cacheItem[i][17] = set_cntr #update set counter
                    elif cacheItem[i][set_cntr] != 0 and cacheItem[i][set_cntr] == entry[0:index_start]: #if not empty & the same
                        HIT += 1
                    else: # cacheItem.tag[0] != "" and cacheItem.tag != entry.tag:
                        cacheItem[i][set_cntr] = entry[0:index_start]
                        MISS += 1
                        set_cntr += 1 #increment spot in set since its filled
                        cacheItem[i][17] = set_cntr #update set counter
                # else: #entry.index != cacheItem.index
                #     MISS += 1
                # break
    #--------------------------------------------------------------
    #-------------------------------------------------------------- 
#     #FIFO
#     #--------------------------------------------------------------
#     # for entry in dataSets:
#     #     for cacheItem in cache:
#     #         if entry.index == cacheItem.index:
#     #             if cacheItem.tag[0] == "":
#     #                 cacheItem.tag = entry.tag
#     #                 MISS += 1
#     #             elif cacheItem.tag[0] != "":
#     #                 cacheItem.tag.append(entry.tag)
#     #                 HIT += 1
#     #             else: # cacheItem.tag[0] != "" and cacheItem.tag != entry.tag:
#     #                 cacheItem.tag.pop(0)
#     #                 cacheItem.tag.append(entry.tag)
#     #                 MISS += 1
#     #         else: #entry.index != cacheItem.index
#     #             MISS += 1  
#     #         break
                    



    #Output results
    total = MISS + HIT
    print("Misses: %d\nHits: %d" % (MISS, HIT))
    print("Miss Rate: %f \nHit Rate: %f" % ((MISS/(total*10)), (HIT/(total*10))))
    print("Total Number of References = %d" % (total))
    # print("Miss rate = %f" % (MISS/600000))
    # print("Hit rate = %f" % (HIT/600000))



main()