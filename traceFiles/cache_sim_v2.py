#32 sets, 1-way set associative (Direct mapped)
#8 contingous addresses per line
#each memory reference is a 3 byte word
#

import math

def set_counter(index_loc, N, cache):
    set_cntr = int(cache[index_loc][N+1])

    if(set_cntr == N):
        set_cntr = 1 #set to 1 bc location 0 in the list is the "index" val
    else:
        set_cntr += 1
    cache[index_loc][N+1] = set_cntr #where the set_cntr val is stored


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


    #lower 3 bits are cleared so, ignore bits 21-23

    index_size = int(math.log2(K)) # 1,2,3,4
    index_start = 21 - index_size
    #index = entry[index_start:21] #21 is stop bit, not included

    # offset = entry[:]
    # offsets.append(offset)
    #offset probably not used due to removal of last 3 bits,
    #as stated in handout

    #tag = entry[0:index_start] #setting tag

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

     #print(cache[0][0])
        

    # #-------------------------------------------------------------
    # #old LRU
    # #-------------------------------------------------------------
    # for entry in reorderedData:
    #     for cacheItem in cache:
    #         for i in range(N):
    #             set_cntr = 0 #variable for counting spot in set
    #             if cacheItem[i][0] == entry[index_start:21]: #if the index of the trace data == the index of the cache
    #                 if cacheItem[i][set_cntr] == 0: #if the space is empty
    #                     cacheItem[i][set_cntr] = entry[0:index_start] #fill empty space with tag
    #                     MISS += 1
    #                     set_cntr += 1 #increment spot in set since its filled
    #                     cacheItem[i][N-2] = set_cntr #update set counter
    #                 elif cacheItem[i][set_cntr] != 0 and cacheItem[i][set_cntr] == entry[0:index_start]: #if not empty & the same
    #                     HIT += 1
    #                 else: # cacheItem.tag[0] != "" and cacheItem.tag != entry.tag:
    #                     cacheItem[i][set_cntr] = entry[0:index_start]
    #                     MISS += 1
    #                     set_cntr += 1 #increment spot in set since its filled
    #                     cacheItem[i][N-2] = set_cntr #update set counter
    #             # else: #entry.index != cacheItem.index
    #             #     MISS += 1
    #             # break
    # #--------------------------------------------------------------

    empty = 0
    hit = 0
    overwrite = 0
    #-------------------------------------------------------------
    #new LRU
    #-------------------------------------------------------------
    set_cntr = 1 #variable for counting spot in set
    i = 0
    for entry in reorderedData:
        for i in range(K):
            if cache[i][0] == entry[index_start:21]: #if the index of the trace data == the index of the cache
                if cache[i][set_cntr] == 0: #if the space is empty
                    cache[i][set_cntr] = entry[0:index_start] #fill empty space with tag
                    MISS += 1
                    set_counter(i, N, cache) #increment and check set counter
                    empty += 1
                    print(i)
                elif cache[i][set_cntr] != 0 and cache[i][set_cntr] == entry[0:index_start]: #if not empty & the same
                    HIT += 1
                    #set_counter(i, N, cache) #increment and check set counter
                    hit += 1
                else: # cacheItem.tag[0] != "" and cacheItem.tag != entry.tag:
                    cache[i][set_cntr] = entry[0:index_start]
                    MISS += 1
                    set_counter(i, N, cache)
                    overwrite += 1

            # else: #entry.index != cacheItem.index
            #     MISS += 1
            # break
    #--------------------------------------------------------------

    print('[%s]' % ', '.join(map(str, cache)))
    print("empty:", empty)
    print("hit:", hit)
    print("overwrite:", overwrite)

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