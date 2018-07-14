# Memorize.py
Memorize.py is a Python decorator for caching a function's results in local storage. 

## What's the point?
In many situations, recycling the output of a function is more efficient than running the function multiple times. A [typical memoizing decorator](https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize) does exactly that for as long as a program is running (the output is stored in Python variable space). Memorize.py stores the output as a .cache file in the current (or target file's) directory for reuse in future program executions. If the Python file containing the decorated function has changed since the last run, the current cache is deleted and a new cache is created (in case the behavior of the function has changed).

## Danger zone!
**BEWARE**: only [pure functions](http://www.sitepoint.com/functional-programming-pure-functions/) should be memoized! 
Otherwise you might encounter unexpected results.  
* Does your function have any external effects? (writing to a file, printing to the console, changing a global variable...)
* Does the function depend on anything outside of the current file that may have changed (external classes, methods, functions, or data)?

## Unfinished business
Don't use this for functions whose arguments can't be dictionary keys (such as lists). I'd like to add support for this in the future.

## Install

```shell
pip install memorize.py
```

or

```shell
pip install git+https://github.com/brmscheiner/memorize.py.git#egg=memorize
```

## Usage 

```
from memorize import Memorize

@Memorize
def yourFunction(x, y, z):
  # do great things...
```
