
try:
    pass
except BaseException:  # bad # B036: 0
    print("aaa")
    pass


try:
    pass
except BaseException as ex:  # bad # B036: 0
    print(ex)
    pass


try:
    pass
except ValueError:
    raise
except BaseException:  # bad # B036: 0
    pass


try:
    pass
except BaseException:  # ok - reraised
    print("aaa")
    raise


try:
    pass
except BaseException as ex:  # bad - raised something else # B036: 0
    print("aaa")
    raise KeyError from ex

try:
    pass
except BaseException as e:
    raise e  # ok - raising same thing

try:
    pass
except BaseException:
    if 0:
        raise  # ok - raised somewhere within branch

try:
    pass
except BaseException: # B036: 0
    try:  # nested try
        pass
    except ValueError:
        raise  # bad - raising within a nested try/except, but not within the main one

try:
    pass
except BaseException: # B036: 0
    raise a.b from None  # bad (regression test for #449)
