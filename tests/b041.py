a = 1
test = {'yes': 1, 'yes': 1}
test = {'yes': 1, 'yes': 1, 'no': 2, 'no': 2}
test = {'yes': 1, 'yes': 1, 'yes': 1}
test = {1: 1, 1.0: 1}
test = {True: 1, True: 1}
test = {None: 1, None: 1}
test = {a: a, a: a}

# no error if either keys or values are different
test = {'yes': 1, 'yes': 2}
test = {1: 1, 2: 1}
test = {(0, 1): 1, (0, 2): 1}
test = {(0, 1): 1, (0, 1): 2}
b = 1
test = {a: a, b: a}
test = {a: a, a: b}
class TestClass:
    pass
f = TestClass()
f.a = 1
test = {f.a: 1, f.a: 1}


