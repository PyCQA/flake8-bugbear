import functools

for i in range(10):
    print(i)

print(i)  # name no longer defined on Python 3; no warning yet

for i in range(10):  # name not used within the loop; B007  # B007: 4, "i"
    print(10)

print(i)  # name no longer defined on Python 3; no warning yet


for _ in range(10):  # _ is okay for a throw-away variable
    print(10)


for i in range(10):
    for j in range(10):
        for k in range(10):  # k not used, i and j used transitively  # B007: 12, "k"
            print(i + j)


def strange_generator():
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for l in range(10):
                    yield i, (j, (k, l))


for i, (j, (k, l)) in strange_generator():  # i, k not used  # B007: 4, "i"  # B007: 12, "k"
    print(j, l)


# A loop variable read by a function defined in the same scope is used (#175).
def closure_defined_before_loop():
    def f(x):
        print(i, x)

    for i in [1, 2, 3]:
        f("HI")


def closure_defined_after_loop():
    for i in [1, 2, 3]:
        pass

    def f():
        return i

    return f


def lambda_reads_loop_variable():
    for i in range(3):
        pass
    return lambda: i


def closure_in_other_block():
    if True:

        def f():
            print(i)

    for i in range(3):
        f()


def nested_closure_reads_through_enclosing_function():
    def outer():
        def inner():
            print(i)

        return inner

    for i in range(3):
        outer()


def closure_reads_in_comprehension_iterable():
    def f():
        return [x for x in i]

    for i in range(3):
        f()


def method_reads_loop_variable():
    class C:
        def method(self):
            return i

    for i in range(3):
        C()


def nonlocal_read():
    def f():
        nonlocal i
        i += 1

    for i in range(3):
        f()


def closure_that_assigns_its_own_variable():
    def f():
        i = 1
        return i

    for i in range(3):  # B007: 8, "i"
        f()


def closure_with_parameter_of_the_same_name(i):
    def f(i):
        return i

    for i in range(3):  # B007: 8, "i"
        f(1)


def closure_with_lambda_parameter_of_the_same_name():
    f = lambda i: i

    for i in range(3):  # B007: 8, "i"
        f(1)


def closure_with_local_assigned_after_read():
    def f():
        print(i)
        i = 1

    for i in range(3):  # B007: 8, "i"
        f()


def closure_with_comprehension_variable_of_the_same_name():
    def f():
        return [i for i in range(3)]

    for i in range(3):  # B007: 8, "i"
        f()


def closure_with_loop_of_the_same_name():
    def f():
        for i in range(3):
            print(i)

    for i in range(3):  # B007: 8, "i"
        f()


def closure_with_import_of_the_same_name():
    def f():
        import i

        return i

    for i in range(3):  # B007: 8, "i"
        f()


def closure_with_global_declaration():
    # `g` in `f` is the module-level variable, not the loop variable
    def f():
        global g
        return g

    for g in range(3):  # B007: 8, "g"
        f()


def class_scope_variable_is_not_the_loop_variable():
    class C:
        i = 1
        j = i

    for i in range(3):  # B007: 8, "i"
        C()


def function_in_other_scope_does_not_count():
    def other():
        return n

    def loops():
        for n in range(3):  # B007: 12, "n"
            pass

    return other, loops


def one_of_two_variables_is_read_by_the_closure():
    def f():
        return j

    for i, j in enumerate("ab"):  # B007: 8, "i"
        f()


async def async_closure_reads_loop_variable():
    async def f():
        return i

    for i in range(3):
        await f()


def class_body_in_closure_reads_loop_variable():
    def f():
        class C:
            x = i

        return C

    for i in range(3):
        f()


def closure_that_binds_the_name_in_other_ways():
    def with_as():
        with open("f") as i:
            return i

    def except_as():
        try:
            pass
        except ValueError as i:
            return i

    def walrus():
        if (i := 1):
            return i

    def def_name():
        def i():
            pass

        return i

    for i in range(3):  # B007: 8, "i"
        with_as()
        except_as()
        walrus()
        def_name()


def closure_reads_in_nested_definitions():
    def f():
        @decorator(i)
        def g(x=i, *, y=i):
            pass

        class C(Base, metaclass=i):
            pass

        return {k: v for k, v in i if v}, {*i}

    for i in range(3):
        f()


def closure_reads_in_dict_comprehension_only():
    def f():
        return {k: i for k in "ab"}

    for i in range(3):
        f()


def closure_shadows_in_dict_comprehension():
    def f():
        return {i: i for i in "ab"}

    for i in range(3):  # B007: 8, "i"
        f()


@staticmethod
@functools.cache
def decorated_scope_with_closure():
    def f():
        return i

    for i in range(3):
        f()


def global_loop_variable_read_by_closure():
    global gi

    def f():
        return gi

    for gi in range(3):
        f()


def global_loop_variable_read_by_deeply_nested_closure():
    global gh

    def g():
        def h():
            return gh

        return h

    for gh in range(3):
        g()


def global_loop_variable_shadowed_by_intermediate_local():
    global go

    def mid():
        go = 5

        def inner():
            return go

        return inner

    for go in range(3):  # B007: 8, "go"
        mid()


def global_loop_variable_shadowed_by_comprehension():
    global gc

    def f():
        return [gc for gc in range(3)]

    for gc in range(3):  # B007: 8, "gc"
        f()
