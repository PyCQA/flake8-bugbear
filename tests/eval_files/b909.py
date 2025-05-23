"""
Should emit:
B999 - on lines 11, 25, 26, 40, 46
"""

# lists

some_list = [1, 2, 3]
some_other_list = [1, 2, 3]
for elem in some_list:
    # errors
    some_list.remove(elem) # B909: 4
    del some_list[2] # B909: 4
    some_list.append(elem) # B909: 4
    some_list.sort() # B909: 4
    some_list.reverse() # B909: 4
    some_list.clear() # B909: 4
    some_list.extend([1, 2]) # B909: 4
    some_list.insert(1, 1) # B909: 4
    some_list.pop(1) # B909: 4
    some_list.pop() # B909: 4

    # conditional break should error
    if elem == 2:
        some_list.remove(elem) # B909: 8
        if elem == 3:
            break

    # non-errors
    some_other_list.remove(elem)
    del some_list
    del some_other_list
    found_idx = some_list.index(elem)
    some_list = 3

    # unconditional break should not error
    if elem == 2:
        some_list.remove(elem)
        break


# dicts
mydicts = {'a': {'foo': 1, 'bar': 2}}

for elem in mydicts:
    # errors
    mydicts.popitem() # B909: 4
    mydicts.setdefault('foo', 1) # B909: 4
    mydicts.update({'foo': 'bar'}) # B909: 4

    # no errors
    elem.popitem()
    elem.setdefault('foo', 1)
    elem.update({'foo': 'bar'})

# sets

myset = {1, 2, 3}

for _ in myset:
    # errors
    myset.update({4, 5}) # B909: 4
    myset.intersection_update({4, 5}) # B909: 4
    myset.difference_update({4, 5}) # B909: 4
    myset.symmetric_difference_update({4, 5}) # B909: 4
    myset.add(4) # B909: 4
    myset.discard(3) # B909: 4

    # no errors
    del myset


# members
class A:
    some_list: list

    def __init__(self, ls):
        self.some_list = list(ls)


a = A((1, 2, 3))
# ensure member accesses are handled
for elem in a.some_list:
    a.some_list.remove(elem) # B909: 4
    del a.some_list[2] # B909: 4


# Augassign

foo = [1, 2, 3]
bar = [4, 5, 6]
for _ in foo:
    foo *= 2 # B909: 4
    foo += bar # B909: 4
    foo[1] = 9 #todo # B909: 4
    foo[1:2] = bar # B909: 4
    foo[1:2:3] = bar # B909: 4

foo = {1,2,3}
bar = {4,5,6}
for _ in foo:
    foo |= bar # B909: 4
    foo &= bar # B909: 4
    foo -= bar # B909: 4
    foo ^= bar # B909: 4


# more tests for unconditional breaks
for _ in foo:
    foo.remove(1)
    for _ in bar:
        bar.remove(1)
        break
    break

# should not error
for _ in foo:
    foo.remove(1)
    for _ in bar:
        ...
    break

# should error (?)
for _ in foo:
    foo.remove(1) # B909: 4
    if bar:
        bar.remove(1)
        break
    break

lst: list[dict] = [{}, {}, {}]
for dic in lst:
    dic["key"] = False # no error



for grammar in grammars:
    errors[grammar.version] = InvalidInput() # no error



for key in self.hpo_params:
    if key in nni_config:
        nni_config[key] = self.hpo_params[key] # no error


some_dict = {"foo": "bar"}
for key in some_dict:
    some_dict[key] = 3 # no error

for key in some_dict.keys():
    some_dict[key] = 3 # no error
