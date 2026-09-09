"""
Should emit:
B020 - on lines 8, 21, 32, 36, 58, and 75
"""

items = [1, 2, 3]

for items in items:  # B020: 4, "items"
    print(items)

items = [1, 2, 3]

for item in items:
    print(item)

values = {"secret": 123}

for key, value in values.items():
    print(f"{key}, {value}")

for key, values in values.items():  # B020: 9, "values"
    print(f"{key}, {values}")

# Variables defined in a comprehension are local in scope
# to that comprehension and are therefore allowed.
for var in [var for var in range(10)]:
    print(var)

for var in (var for var in range(10)):
    print(var)

for k, v in {k: v for k, v in zip(range(10), range(10, 20))}.items():  # B905: 30
    print(k, v)

# However we still call out reassigning the iterable in the comprehension.
for vars in [i for i in vars]:  # B020: 4, "vars"
    print(vars)

for var in sorted(range(10), key=lambda var: var.real):
    print(var)


# `for self.a.b in self.c` rebinds an attribute, not the name `self`: two
# different attributes of the same object are two different bindings.
# https://github.com/PyCQA/flake8-bugbear/issues/248
class AttributeTargets:
    test_suite = [1, 2, 3]

    def ok_sibling_attributes(self):
        for self.model_instance.value in self.test_suite:
            print(self.model_instance.value)

    def ok_plain_attribute(self):
        for self.value in self.test_suite:
            print(self.value)

    def still_an_error(self):
        for self.test_suite in self.test_suite:  # B020: 12, "self.test_suite"
            print(self.test_suite)

# the `obj` a comprehension binds is not the `obj` the loop rebinds
def ok_comprehension_scope(obj, objects):
    for obj.value in [obj.value for obj in objects]:
        print(obj.value)


# nor is the `obj` a lambda binds
def ok_lambda_scope(obj, objects):
    for obj.value in map(lambda obj: obj.value, objects):
        print(obj.value)


# the same path on both sides is still an error
def still_an_error_at_module_level(obj):
    for obj.value in obj.value:  # B020: 8, "obj.value"
        print(obj.value)
