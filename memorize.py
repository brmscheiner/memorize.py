import collections, functools, pickle, inspect
import os.path, sys, re, unicodedata
''' 
memorize.py is a simple decorator for memoizing a 
function across multiple program executions.

A function decorated with @memorize caches its return 
value every time it is called. If the function is called 
later with the same arguments, the cached value is 
returned (the function is not reevaluated). The cache is 
stored as a .cache file in the current directory for reuse 
in future executions. If the Python file containing the 
decorated function has been updated since the last run, 
the current cache is deleted and a new cache is created 
(in case the behavior of the function has changed).

BEWARE: only pure functions should be memoized! 
Otherwise you might encounter unexpected results. Ask 
yourself: 
 - does your function alter a global object?
 - do you need to see the result of print statements?
 - does the result of the function depend on something 
 outside of the application that may have changed (such
 as http requests, or  functions that use external classes, 
 methods, or functions)?

DO NOT use this decorator if you are planning on 
running multiple instances of the memoized function 
concurrently. If there is sufficient interest this feature 
may be supported in the future.

DO NOT use this decorator for functions that take 
arguments that cannot be dictionary keys (such as lists). 
Since the cache is stored internally as a dictionary, 
no information will be cached and no memoization will 
take place.
'''

class memoized(object):
    def __init__(self, func):
        self.func = func
        self.setParentFile() # sets self.parent_filepath and self.parent_filename
        self.__name__ = self.func.__name__
        self.setCacheFilename() 
        if self.cacheExists():
            self.readCache() # sets self.timestamp and self.cache 
            if not self.isSafeCache():
                self.cache = {}
        else:
            self.cache = {}
        
    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            self.saveCache()
            return value
        
    def setParentFile(self):
        '''
        Sets self.parent_file to the absolute path of the 
        file containing the memoized function. 
        '''
        rel_parent_file = inspect.stack()[-1].filename
        self.parent_filepath = os.path.abspath(rel_parent_file)
        self.parent_filename = filenameFromPath(rel_parent_file)
        
    def setCacheFilename(self):
        ''' 
        Sets self.cache_filename to an os-compliant 
        version of "file_function.cache" 
        '''
        filename = slugify(self.parent_filename.replace('.py',''))
        funcname = slugify(self.__name__)
        self.cache_filename = filename+'_'+funcname+'.cache'
        
    def getLastUpdate(self):
        ''' 
        Returns the time that the parent file was last 
        updated.
        '''
        last_update = os.path.getmtime(self.parent_filepath)
        return last_update
        
    def isSafeCache(self):
        ''' 
        Returns True if the file containing the memoized 
        function has not been updated since the cache was 
        last saved. 
        '''
        if self.getLastUpdate() > self.timestamp:
            return False
        return True
            
    def readCache(self):
        ''' 
        Read a pickled dictionary into self.timestamp and 
        self.cache. See self.saveCache. 
        '''
        with open(self.cache_filename,'rb') as f:
            data = pickle.loads(f.read())
            self.timestamp = data['timestamp']
            self.cache = data['cache']
            
    def saveCache(self):
        ''' 
        Pickle the file's timestamp and the function's cache 
        in a dictionary object. 
        '''
        with open(self.cache_filename,'wb+') as f:
            out = dict()
            out['timestamp'] = self.getLastUpdate()
            out['cache'] = self.cache
            f.write(pickle.dumps(out))

    def cacheExists(self):
        if os.path.isfile(self.cache_filename):
            return True
        return False

    def __repr__(self):
       ''' Return the function's docstring. '''
       return self.func.__doc__

    def __get__(self, obj, objtype):
        ''' Support instance methods. '''
        return functools.partial(self.__call__, obj)
        
def slugify(value):
    '''
    Normalizes string, converts to lowercase, removes 
    non-alpha characters, and converts spaces to 
    hyphens. From Django's source code.
    See http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
    '''
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    if sys.version_info[0] < 3:
        value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
        value = unicode(re.sub('[-\s]+', '-', value))
    else: # unicode function doesnt exist in python 3
        value = re.sub('[^\w\s-]', '', value.decode('utf-8','ignore')).strip().lower()
        value = re.sub('[-\s]+', '-', value)
    return value
    
def filenameFromPath(filepath):
    return filepath.split('/')[-1]
        
