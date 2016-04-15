from memorize import Memorize
import random, time

@Memorize
def test_memorize(x):
    time.sleep(1)
    return x
        
if __name__=='__main__':
    for x in range(3):
        print(test_memorize(x))