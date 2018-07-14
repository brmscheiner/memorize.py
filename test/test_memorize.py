from memorize import Memorize
import time


@Memorize
def test_memorize(x):
    print('invoked original test_memorize!')
    time.sleep(1)
    return x


if __name__ == '__main__':
    for x in range(3):
        print(test_memorize(x))
    for x in range(3):
        print(test_memorize(x))
