def closure_reads_loop_variable_in_match():
    def f(x):
        match x:
            case [1, i]:
                return i
            case {"k": rest, **i}:
                return rest
        return 0

    def g():
        return i

    for i in range(3):
        g()


def closure_binds_the_name_in_a_pattern():
    def f(x):
        match x:
            case [1, i]:
                return i
        return 0

    for i in range(3):  # B007: 8, "i"
        f(1)
