def arbitrary_fun(*args, **kwargs): ...


# classic case
try:
    ...
except Exception as e:
    e.add_note("...")  # error

try:
    ...
except Exception as e:  # safe (other linters will catch this)
    pass

try:
    ...
except Exception as e:
    e.add_note("...")
    raise  # safe

# other exception raised
try:
    ...
except Exception as e:
    f = ValueError()
    e.add_note("...")  # error
    raise f

# raised as cause
try:
    ...
except Exception as e:
    f = ValueError()
    e.add_note("...")  # safe
    raise f from e

# assigned to other variable
try:
    ...
except Exception as e:
    e.add_note("...")  # safe
    foo = e

# "used" in function call
try:
    ...
except Exception as e:
    e.add_note("...")  # safe
    # not that printing the exception is actually using it, but we treat
    # it being used as a parameter to any function as "using" it
    print(e)

try:
    ...
except Exception as e:
    e.add_note("...")  # safe
    list(e)

# kwarg
try:
    ...
except Exception as e:
    e.add_note("...")  # safe
    arbitrary_fun(kwarg=e)

# stararg
try:
    ...
except Exception as e:
    e.add_note("...")  # safe
    arbitrary_fun(*(e,))

try:
    ...
except Exception as e:
    e.add_note("...")  # safe
    arbitrary_fun(**{"e": e})


# multiple ExceptHandlers
try:
    ...
except ValueError as e:
    e.add_note("")  # error
except TypeError as e:
    raise e

# exception variable used before `add_note`
mylist = []
try:
    ...
except Exception as e: # safe
    mylist.append(e)
    e.add_note("")


# AnnAssign
try:
    ...
except Exception as e:  # safe
    e.add_note("")
    ann_assign_target: Exception = e

# special case: e is only used in the `add_note` call itself
try:
    ...
except Exception as e:  # error
    e.add_note(str(e))
    e.add_note(str(e))

# check nesting
try:
    ...
except Exception as e:  # error
    e.add_note("")
    try:
        ...
    except ValueError as e:
        raise

# questionable if this should error
try:
    ...
except Exception as e:
    e.add_note("")
    e = ValueError()

# *** unhandled cases ***


# This should ideally error
def exc_add_note_not_in_except():
    exc = ValueError()
    exc.add_note("")


# but not this
def exc_add_note_not_in_except_safe(exc: ValueError):
    exc.add_note("")


# we currently only check the target of the except handler, even though this clearly
# is hitting the same general pattern. But handling this case without a lot of false
# alarms is very tricky without more infrastructure.
try:
    ...
except Exception as e:
    e2 = ValueError()  # should error
    e2.add_note(str(e))


def foo_add_note_in_excepthandler():
    e2 = ValueError()
    try:
        ...
    except Exception as e:
        e2.add_note(str(e))  # safe
    raise e2


# We don't currently handle lambdas or function definitions inside the exception
# handler. This isn't conceptually difficult, but not really worth it with current
# infrastructure
try:
    ...
except Exception as e:  # should error
    e.add_note("")
    f = lambda e: e

try:
    ...
except Exception as e:  # should error
    e.add_note("")

    def habla(e):
        raise e


# We also don't track other variables
try:
    ...
except Exception as e:
    e3 = e
    e3.add_note("")  # should error
