# memorize.py
Simple decorator for memoizing a function across multiple program executions.

## Wait, what?
A function decorated with @Memorize saves/remembers/caches its return value every time it is called. If the function is called 
later with the same arguments, the cached value is returned (the function is not reevaluated). This process is called **memoization**. 
Memorize.py does a little more than a [typical memoizing decorator](https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize) because it stores the cache as a .cache file in the current directory for reuse in future program executions. If the Python file containing the 
decorated function has been updated since the last run, the current cache is deleted and a new cache is created (in case the behavior of the function has changed).

## Danger zone!
**BEWARE**: only [pure functions](http://www.sitepoint.com/functional-programming-pure-functions/) should be memoized! 
Otherwise you might encounter unexpected results. Ask 
yourself: 
* Does your function alter a global object?
* Do you need to see the result of print statements?
* Does the result of your function depend on something outside of the application that may not behave like it used to (external classes, methods, functions, or data)?

**DO NOT** use this decorator if you are planning on running multiple instances of the memoized function concurrently. If there is sufficient interest this feature may be supported in the future.

**DO NOT** use this decorator for functions that take arguments that cannot be dictionary keys (such as lists). Since the cache is stored internally as a dictionary, no information will be cached and no memoization will take place.

