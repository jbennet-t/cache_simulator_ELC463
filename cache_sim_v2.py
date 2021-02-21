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
    #cache[index_loc][N+1] = set_cntr #where the set_cntr val is stored

    return(set_cntr)


def cache_main(trace_file, KN, K, N, method):
    data = []
    # KN
    # K # number of lines(blocks) per set
    # N # number of sets
    # L = 8 # number of bytes per line(block) of cache mem

    HIT = 0
    MISS = 0

    #Read memory references from trace file and store every byte as a string of bits in a list
    #Currently using TRACE1.DAT -> change for trace file as neccesary
    with open(trace_file, "rb") as file:
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

        

    #-------------------------------------------------------------
    #LRU
    #-------------------------------------------------------------
    set_cntr = 1 #variable for counting spot in set
    i = 0
    j = 0
    for entry in reorderedData:
        for i in range(K):
            if cache[i][0] == entry[index_start:21]: #if the index of the trace data == the index of the cache
                k = 1
                hit_flg = 0
                for k in range(N+1): #1 - N
                    if (cache[i][k] == entry[0:index_start]):
                        hit_flg = 1

                if cache[i][set_cntr] == 0: #if the space is empty
                    cache[i][set_cntr] = entry[0:index_start] #fill empty space with tag
                    MISS += 1
                    set_cntr = set_counter(i, N, cache) #increment and check set counter
                    cache[i][N+1] = set_cntr
                    #print(set_cntr)
                elif cache[i][set_cntr] != 0 and hit_flg == 1: #if not empty & the same
                    HIT += 1
                    if method == 0: #if LRU
                        set_cntr = set_counter(i, N, cache) #increment and check set counter
                        cache[i][N+1] = set_cntr
                    #otherwise, don't for FIFO
                else:
                    cache[i][set_cntr] = entry[0:index_start]
                    MISS += 1
                    set_cntr = set_counter(i, N, cache) #increment and check set counter
                    cache[i][N+1] = set_cntr


    #--------------------------------------------------------------

    #print('[%s]' % ', '.join(map(str, cache)))


    #Output results
    total = MISS + HIT
    MISS_RATE = ((MISS/total)*10)
    # print("Misses: %d\nHits: %d" % (MISS, HIT))
    # print("Miss Rate: %f \nHit Rate: %f" % ((MISS/(total*10)), (HIT/(total*10))))
    # print("Total Number of References = %d" % (total))

    return(MISS,MISS_RATE)




def main():
    KN_value = [64,256]                                                  # def KN
    K_value = [2,4,8,16]                                                # def K
    method = [0,1]                                                         # Type LRU or FIFO
    filename = ["traceFiles/TRACE1.DAT","traceFiles/TRACE2.DAT"]           # Trace File

    test_num = 1
    with open('output_cache.txt', 'wt') as out:
        out.write("Test #\tTrace\tType\tKN\tK\tMisses\tMiss Rate\n")# Save in txt

        for x in range(2):
            for v in method:
                for i in KN_value:
                    for j in K_value:
                        N_value = int(i/j)
                        miss_count, miss_rate = cache_main(filename[x], i, j, N_value, v)
                        out.write("%d\t%d\t%d\t%d\t%d\t%d\t%f\n" % (test_num,x,v,i,j,miss_count,miss_rate))
                        test_num += 1



main()