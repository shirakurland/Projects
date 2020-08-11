from BitVector import BitVector
from BitHash import BitHash
import pytest

class CountingBloomFilter(object):
    
    # find bits per cell: 2**n -1 = max count for each cell
    # n is the number of bits per cell 
    # loop to try solving for n - keep going higher until you reach a number thats >= maxcount
    def __numBitsPerCell(self, maxCount):
        numBitsPerCell = 0
        
        while (2**numBitsPerCell) -1 < maxCount:
            numBitsPerCell+=1
            
        # once you've fallen out of the loop, the number of bits per cell is >= to the maxCount
        return numBitsPerCell

    # returns the number of bitsNeeded for this CBF
    def __bitsNeeded(self, numBitsPerCell, numCells):
        # get the total bits needed by mulitplying bits per cell and 
        # the total number of cells speciifed by client        
        return  int(numBitsPerCell * numCells)
    
    # Create a Counting Bloom Filter that will keep track 
    # of the number of inserted keys, using numHashes hash 
    # functions, and that will count each key up to the maxCount.
    # All attributes must be private.
    def __init__(self, numCells, numHashes, maxCount):
        # will need to use __numBitsPerCell to find the number of bits per cell needed
        self.__bitsPC = self.__numBitsPerCell(maxCount)
          
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        self.__N = self.__bitsNeeded(self.__bitsPC,numCells)
        
        #bitvector
        self.__BV = BitVector(size = self.__N)
        
        #numhashes
        self.__numHashes = numHashes
        
        #numCells
        self.__numCells = numCells
        
        #maxCount
        self.__maxCount = maxCount
        
        #keys inserted - this was part of the false positive rate eq therefore i dont need right?
        self.__numInserted = 0
        
    # insert the specified key into the Counting Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Counting Bloom Filter always succeeds!
    def insert(self, key):
        
        # by default it will be zero 
        hashval = 0
        
        # for each i, bithash the key for the hashval which will be the prev hashval 
        for i in range(self.__numHashes): #loop numHashes times
            
            hashval = BitHash(key, hashval)
    
            # mod by the number of cells
            moddedHashval = hashval % self.__numCells
            
            # extract the binary value of the location of insertion: 
            # to do this, slice the bit vector starting at the moddedHashval times the number of bits per cell,
            # up until that number, plus the number of bits per cell minus 1
            # for example, if it was a 4 bit cell and the moddedHashval was 2, you want to set the 8th-11th bits of the BV
            
            # i is the start of my slice
            i = moddedHashval*self.__bitsPC
            
            # j is where I'm slicing until
            j = i + self.__bitsPC
            
            # save the current binary val of the location you will later be updating 
            curBinaryVal = self.__BV[i:j]
            
            # switch the value from binary to int: 
            # to do this, use the in_val() method
            integerVal = curBinaryVal.int_val()
            
            # incrememnt the value of this location by 1, assuming the number will 
            # be less than or equal to the limit specified by user(maxCount)
            if integerVal < self.__maxCount: 
                integerVal+=1
            
            # switch back to binary value so we can update the CBF appropriately: 
            # to do this, construct a small bv from the incremented integer above
            bv2 = BitVector(intVal = integerVal, size = len(self.__BV[i:j]))
           
            # update the value at location of insertion 
            # assign the small bv2 back into the specified slice of bits in the main BitVector
            self.__BV[i:j] = bv2
         
         # you dont need to return anything because it always succeeds    
   
    # the find method Returns True if key has been inserted into the CBF n or more times. 
    # Returns False otherwise 
    def find(self, key, n = 1):
        hashval = 0
        
        # set the default value of the minimum hash to the maxCount
        # as you find each hash of the key, update the minVal to the accurate min
        minVal = self.__maxCount
        
        # loop through all locations of the key to get the minVal of the key
        for i in range(self.__numHashes):
            hashval = BitHash(key, hashval)
            moddedHashval = hashval % self.__numCells
            
            # get the slice of the BV where the key will be found
            i = moddedHashval*self.__bitsPC
            j = i + self.__bitsPC
              
            curBinaryVal = self.__BV[i:j]
        
            # switch the value from binary to int to see how many times the key was inserted in int form
            # to do this, use the in_val() method
            integerVal = curBinaryVal.int_val()
            
            # if the current cell has a val that's lower than minVal, update minVal
            if integerVal < minVal: 
                minVal = integerVal
                        
        # if inserted n or more times meaning minVal >= n, return True 
        if minVal >=n: return True
        
        # return False otherwise
        return False
       
    # delete function - delete one occurance per bit of the key
    # to delete one occurance of the key, loop through numHashes and decrement each hash by one     
    def delete(self, key):
        
        # by default it will be zero 
        hashval = 0
        
        # for each i, bithash the key for the hashval which will be the prev hashval    
        for i in range(self.__numHashes): #loop numHashes times
           
            hashval = BitHash(key, hashval)
            moddedHashval = hashval % self.__numCells
              
            # extract the binary value of the location of insertion
            # slice locations are i to j-1
            i = moddedHashval*self.__bitsPC
            j = i + self.__bitsPC
            
            curBinaryVal = self.__BV[i:j]
            
            # switch the value from binary to int
            # to do this, use the in_val() method
            integerVal = curBinaryVal.int_val()
          
            # decrement by 1, never allowing the value to go below zero
            if integerVal > 0: 
                integerVal-=1
                
            # switch back to binary value
            # construct a small bv from the decremented integer above
            bv2 = BitVector(intVal = integerVal, size =len(self.__BV[i:j]))
            
            # update the value at location of deletion
            # assign the small bv2 back into the specified slice of bits in the main BitVector
            self.__BV[i:j] = bv2
            
# implement pytests to check the methods work accurately

# test that the insert will not insert more keys than the max count
def test_maxCountInsert():
    numCells = 8
    numHashes = 5
    maxCount = 15
    numKeys = 90 
    BV = CountingBloomFilter(numCells,numHashes,maxCount)
    d = {}
    
    # insert 90 keys into the Counting Bloom Filter
    # the maxCount is 15, only 15 keys should be inserted 
    for i in range(numKeys):
        key = "shira"
        BV.insert(key)
        
    # make sure there is not at least 90 instances of the key
    assert BV.find("shira",90) == False
    # make sure there are at least 15 instances of the key 
    assert BV.find("shira",15) == True

# throw a lot of keys in the CBF and make sure they all are inserted
def test_insertManyKeys():
    numCells = 6
    numHashes = 2
    maxCount = 15
    numKeys = 1000 
    
    # create the CBF
    BV = CountingBloomFilter(numCells,numHashes,maxCount)    
    d = {}
    
    # read the first numKeys words from the file and insert them 
    # into the CBF. Close the input file.    
    file = open("wordlist.txt")
    for i in range(numKeys):
        key = file.readline()
        BV.insert(key)
        d[key] = 1
    file.close() 
    
    # re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and make sure that if it exists in the dict it is also 
    # present in the CBF  
    file = open("wordlist.txt")
    for i in range(numKeys):
        key = file.readline()

        # make sure there is at least one instance of the key in the CBF that exists in the dict 
        assert BV.find(key) == (d[key] >=1)
    
# test to make sure the keys are actually being inserted 
# by searching to find the correct number of insertions
def test_find():
    numCells = 4
    numHashes = 3
    maxCount = 15
    BV = CountingBloomFilter(numCells,numHashes,maxCount)
    d = {}
    
    # insert keys into the Counting Bloom Filter
    # insert them in the dictionary too
    for i in range(4):
        key = "shira"
        BV.insert(key)
        if key in d: 
            d[key] += 1
        else: d[key] = 1
    for i in range(15):
        key = "jacob"
        BV.insert(key)
        if key in d: 
            d[key] += 1
        else: d[key] = 1        
    
    # assert the number of found keys in the CBF is the same as the number in the dict
    assert BV.find("shira",4) == (d["shira"] == 4)
    assert BV.find("jacob",15) == (d["jacob"] == 15)
    
# test if the delete method successfully deletes a value
def test_delete():
    numCells = 6
    numHashes = 2
    maxCount = 15
    numKeys = 4    
    BV = CountingBloomFilter(numCells,numHashes,maxCount)
    d = {}
    
    # insert keys into the Counting Bloom Filter
    # insert them in the dictionary too
    for i in range(numKeys):
        key = "shira"
        BV.insert(key)
    
    BV.delete("shira")
    # assert that the CBF returns False when it checks if there are at least 4 instances of the key 
    assert BV.find("shira", 4) == False
    
    # assert that there are at least 3 instances of the key
    assert BV.find("shira",3) == True
    
# test to make sure the delete method will not decrement a cell below zero
def test_deleteBelowZero():
    numCells = 10
    numHashes = 5
    maxCount = 15 
    BV = CountingBloomFilter(numCells,numHashes,maxCount)
    d = {}
    
    # insert a key into the Counting Bloom Filter
    # insert it in the dictionary too
    for i in range(1):
        key = "shira"
        BV.insert(key)
    
    BV.delete("shira") 
    # since there was only one key "shira", the below delete method should not decrement the value again
    BV.delete("shira")
    
    # assert that there are exactly zero instances of shira and not -1 instances
    assert BV.find("shira",0) == True
    
# test an empty CBF
def test_emptyCBF():
    numCells = 20
    numHashes = 4
    maxCount = 5
    BV = CountingBloomFilter(numCells,numHashes,maxCount)
    assert BV.find("shira") == False
    
    
pytest.main(["-v", "-s", "countingBloomFilter.py"])