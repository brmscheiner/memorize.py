from memorize import Memorize


@Memorize
def test_memorize_nested(x):
    print('invoked original nested test_memorize!')
    return x
