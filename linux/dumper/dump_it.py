#copy files from source to destination

class backup:
    
    def locateSource(self, source):
        self.source = source
        
        return self.source

    def locateBackup(self, backup):
        self.backup = backup

        return self.backup

    def sourceDict(self): pass

    def destinationDict(self): pass

    def performChecksum(self): 
        #performs a checksum of each image object
        #hashing algo: MD5
        
        import hashlib

        #need source location

    def compareChecksum(self): pass
        #returns dictionary object of backup objects

    def backup(self):
        #recursively add file names to dic object from the source.

        #recursively add files name to dic object from the destination. 

        #perform checksum on source objects

        #perform checksum on destination objects

        #add checksum source objects to local cache database if they don't exist to create rainbow table

        #create a new dict object of new objects that need to be copied
                

        pass

class hashing:
    import hashlib

    def __init__(self):
        from glob import glob
        from multiprocessing import Process

        #need to get image file path for source device 
        #source_dir (list)
        self.source_dir = glob("location")

        #spawn process
        for i in self.source_dir:
            p = Process(target=md5, args=(self.source_dir,))
            p.start()
            p.join()

    def md5(self, source_dir):
        #returns MD5 hash values of source directory
        #return value: key = pathname + filename : value = checksum

        #items = path+filename:checksum
        self.checksum_library = {}

        #for each file in source, get checksum
        for key in self.source_dir:
            with open(key, 'rb') as self.getMD5:
                self.data = self.getMD5.read()
                self.getHash = hashlib.md5(data).hexdigest()

            if key not in self.checksum_library:
                self.checksum_library[key] = {'value': self.getHash}

        return self.checksum_library
                
            
class cacheTable:
    #source material: https://www.blog.pythonlibrary.org/2016/02/25/python-an-intro-to-caching/

    def __init__(self):
        #open/read cache file, write objects to cache{}
        try:
            with open('cache.txt', 'r') as cacheFile:
                self.cache = cacheFile.read()
        except Exception as e:
            print(e)

        #close file
        cacheFile.close()

    def __contains__(self, key):
        #returns true if key is in cache
        
        return key in self.cache
    
    def updateCache(self, key, value):
        
        #update cache with new key:value if it doesn't exist
        if key not in self.cache:
            try:
                self.cache[key] = {'value': value}
            except Exception as e:
                print (e)

        return self.cache

    def writeCache(self):
        import json

        #reconstruct json from obj str -> dict
        self.js = json.loads(self.cache)

        #open file and append cache data
        with open('cache.txt', 'a+') as cacheFile:
            self.cache = cacheFile.read()

        #close file
        cacheFile.close()
