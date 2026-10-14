# A module-level loop variable read by a function is a global used by that function
# (#175). The function may be defined before or after the loop.
def reads_i():
    return i


for i in range(10):
    pass


for j in range(10):
    pass


def reads_j():
    return j


for k in range(10):  # B007: 4, "k"
    pass


def shadows_k(k):
    return k


def assigns_k():
    k = 1
    return k


def declares_global_k():
    global k
    k = 2  # a store is not a use


def reads_global_m():
    return m


def other_scope():
    # `m` is local to this function, the function above reads another variable
    for m in range(10):  # B007: 8, "m"
        pass


for n in range(10):
    pass


def reads_n_with_global():
    global n
    return n
