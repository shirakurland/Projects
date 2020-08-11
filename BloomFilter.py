from BitVector import BitVector
from BitHash import BitHash
import math 

# a bloomfilter is an array of bits
class BloomFilter(object):
    # Return the estimated number of bits needed in a Bloom Filter that 
    # will store numKeys keys, using numHashes hash functions, and that 
    # will have a false positive rate of maxFalsePositive.
    # See Slide 12 for the math needed to do this.  
    # You use equation B to get the desired phi from P and d
    # You then use equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        #eq P phi = (1-P**(1/d))
        phi = (1-maxFalsePositive**(1/numHashes))
        
        #eq D N = (d/(1-phi**(1/n)))
        N = (numHashes/(1-phi**(1/numKeys)))
        
        #n = numKeys
        #d = numHashes
        #P = maxFalsePositive
    
        return math.ceil(N)
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
           
        # size of the bitvector
        self.__N = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        
        # creating the bitvector array 
        self.__BV = BitVector(size = self.__N)
        
        # numhashes
        self.__numHashes = numHashes
        
        # false positive rate
        self.__falsePositive = maxFalsePositive
        
        # keys inserted
        self.__numInserted = 0
        
        # num of bits set
        self.__bitCount = 0
           
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    def insert(self, key):
        
        # increment the number of inserted keys
        self.__numInserted+=1
        # by default it will be zero 
        hashval = 0
        
        # for each i we do a bithash of the key for the hashval which will be the prev hash val
        
        ## for counting bloom filter, no loop
        
        for i in range(self.__numHashes): #loop d times
            # the point is that you keep updating it for the different values 
            # rehash the prev hashval
            hashval = BitHash(key, hashval)
            
            # use the moddedhashval as the "check mark" for your bloom filter 
            moddedHashval = hashval % self.__N   
       
            ## for CBF, increment the count by 1 (and set the hashval positon to whatever number the count is at )
            # only increment bitCount if this position has not yet been accounted for
            if self.__BV[moddedHashval] == 0: self.__bitCount+=1            
            
            self.__BV[moddedHashval] = 1  # set hashval position mod size of BV bit to 1
         
         # you dont need to return anything because it always succeeds    
      
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.   
    def find(self, key):
        hashval = 0
        for i in range(self.__numHashes):
            # get the hash value and then reduce the number 
            hashval = BitHash(key, hashval)
            moddedHashval = hashval % self.__N               
            if self.__BV[moddedHashval] == 0: return False
            
        # after you fall out of the loop, all locations of hashes forsure have the key there
        return True
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero. 
    def falsePositiveRate(self):
        # phi = (1 - (d/ N)) **n
        # P = (1-phi)**d
        # equation c
        phi = (1- (self.__numHashes/self.__N))**self.__numInserted
       # equation a
        P = (1-phi)**self.__numHashes
        return P
        #return 0.0   # replace this line with your code
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        # that will tell us how many bits are set.
        return self.__bitCount
        
def __main():
    
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    BV = BloomFilter(numKeys,numHashes,maxFalse)
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    file = open("wordlist.txt")
    for i in range(numKeys):
        key = file.readline()
        BV.insert(key)
    file.close()

    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    
    
    # why is this zero?
    print("projected false positive rate:", BV.falsePositiveRate())

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file. 
    
    file = open("wordlist.txt")
    missing = 0
    for i in range(numKeys):
        key = file.readline()
        if not BV.find(key):
            missing +=1
    print("missing keys = ",str(missing)) # should be 0 

    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    
    found = 0
    for j in range(numKeys):
        key = file.readline()
        if BV.find(key):
            found +=1

    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    
    # proportion of the num of falsely found keys divided by the total number of keys  
    print("percentage of false positives:",str((found / numKeys) * 100))
       
if __name__ == '__main__':
    __main()       