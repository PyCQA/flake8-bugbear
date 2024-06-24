def arbitrary_fun(*args, **kwargs):
    ...

try:
    ...
except Exception as e:
    e.add_note("...") # error

try:
    ...
except Exception as e:  # safe (handled by most type checkers)
    pass

try:
    ...
except Exception as e:
    e.add_note("...")
    raise # safe

try:
    ...
except Exception as e:
    e.add_note("...")
    raise e # safe

try:
    ...
except Exception as e:
    f = ValueError()
    e.add_note("...") # error
    raise f

try:
    ...
except Exception as e:
    f = ValueError()
    e.add_note("...") # safe
    raise f from e

try:
    ...
except Exception as e:
    e.add_note("...") # safe
    foo = e

try:
    ...
except Exception as e:
    e.add_note("...") # safe
    # not that printing the exception is actually using it, but we treat
    # it being used as a parameter to any function as "using" it
    print(e)

try:
    ...
except Exception as e:
    e.add_note("...") # safe
    list(e)

try:
    ...
except Exception as e:
    e.add_note("...") # safe
    arbitrary_fun(kwarg=e)

try:
    ...
except Exception as e:
    e.add_note("...") # safe
    arbitrary_fun(*(e,))

try:
    ...
except Exception as e:
    e.add_note("...") # safe
    arbitrary_fun(**{"e":e})


try:
    ...
except ValueError as e:
    e.add_note("") # error
except TypeError as e:
    raise e

mylist = []
try:
    ...
except Exception as e:
    mylist.append(e)
    e.add_note("")


def exc_add_note_not_in_except():
    exc = ValueError()
    exc.add_note("") # should maybe error?

try:
    ...
except Exception as e:
    e2 = ValueError()
    e2.add_note("") # should maybe error?
    raise e

try:
    ...
except Exception as e:
    e.add_note("")
    e = ValueError()

try:
    ...
except Exception as e: # should error, but we don't handle lambdas
    e.add_note("")
    f = lambda e: e

try:
    ...
except Exception as e: # safe
    e.add_note("")
    ann_assign_target: Exception = e

try:
    ...
except Exception as e: # should error
    e.add_note(str(e))

try:
    ...
except Exception as e:  # should error
    e.add_note("")
    try:
        ...
    except ValueError as f:
        pass
