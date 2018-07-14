from test_package.test_in_package import test_memorize_nested
import memorize

memorize.USE_CURRENT_DIR = False

if __name__ == '__main__':
    for x in range(3):
        print(test_memorize_nested(x))
    for x in range(3):
        print(test_memorize_nested(x))
